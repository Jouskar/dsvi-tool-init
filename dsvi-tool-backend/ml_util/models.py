import json
import uuid

import numpy as np
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, GEOSGeometry
from scipy.stats import pearsonr
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

from geo.models import FeatureModel, VectorModel, PointModel
from django.contrib.gis.geos import GeometryCollection
from shapely.geometry import shape
from shapely.ops import cascaded_union
from geojson import Feature, FeatureCollection


# GeoDjango has the dumbest, most lacking documentation known to man, second only to React Leaflet.
# Todo check constructor, add a new VectorModel inst for each new geojson file...

class MLModel(models.Model):  # An attempt at the inheritance of the feature model directly
    vector_model = models.ManyToManyField(VectorModel)

    geojson_str = models.TextField()
    name = models.CharField()

    @staticmethod
    def overlap_score(geometry, rest):
        current_geometry = GEOSGeometry(geometry)
        other_geometry = GEOSGeometry(rest)

        intersection = current_geometry.intersection(other_geometry)
        overlap_similarity = intersection.area / current_geometry.area

        return overlap_similarity

    def _calculate_polygon_similarity(self, geometry1, properties1, geometry2, properties2, threshold):
        max_value1 = properties1['max']
        mean_similarity1 = properties1['mean'] / max_value1

        max_value2 = properties2['max']
        mean_similarity2 = properties2['mean'] / max_value2

        overlap_similarity = self.overlap_score(geometry1, geometry2)

        similarity_score = (0.5 / (mean_similarity1 - mean_similarity2)) + 0.5 * overlap_similarity / 100

        return similarity_score

    def generate_similar_polygons_geojson(self, similar_polygons):
        self.name = uuid.uuid4().hex
        feature_collection = {
            "type": "FeatureCollection",
            "features": []
        }

        print(similar_polygons)

        for polygon in similar_polygons:
            geometry1 = polygon["geometry1"]
            geometry2 = polygon["geometry2"]
            similarity_score = polygon["similarity_score"]

            multipolygon = {
                "type": "MultiPolygon",
                "coordinates": [
                    json.loads(geometry1)["coordinates"],
                    json.loads(geometry2)["coordinates"]
                ]
            }

            feature = {
                "type": "Feature",
                "geometry": multipolygon,
                "properties": {
                    "similarity_score": similarity_score
                }
            }

            feature_collection["features"].append(feature)

        with open(self.name + '.geojson', 'w') as f:
            json.dump(feature_collection, f)

        return feature_collection

    # Rewrote to:
    # 1. support as many vector models as needed
    # 2. generate based on overlap and mean as a ratio?
    def calculate_similarity(self, vector_model1, vector_model2, threshold=0.8):
        similar_polygons = []

        features1 = vector_model1.featuremodel_set.all()
        features2 = vector_model2.featuremodel_set.all()

        for feature1 in features1:
            geometry1 = feature1.geometry
            properties1 = feature1.properties

            for feature2 in features2:
                geometry2 = feature2.geometry
                properties2 = feature2.properties

                similarity_score = self._calculate_polygon_similarity(geometry1, properties1, geometry2, properties2,
                                                                      threshold)

                if similarity_score >= threshold:
                    similar_polygons.append({
                        "geometry1": geometry1,
                        "properties1": properties1,
                        "geometry2": geometry2,
                        "properties2": properties2,
                        "similarity_score": similarity_score
                    })
        self.geojson_str = json.dumps(self.generate_similar_polygons_geojson(similar_polygons))

        return self.geojson_str


# Correlation analysis above works great with multipolygon type data, but not much for point data. For that,
# clustering analysis :D
#  (b - a) / max(a, b)
class PointMLModel(models.Model):
    geogson_file = models.FileField(upload_to='clustered_points/')
    point_models = models.ManyToManyField(PointModel)

    # This method is extremely experimental, thats why it is factored out.
    # If possible, allow user to query differing types of eps values.
    @staticmethod
    def calculate_eps(self, point_models, k=3):
        data = np.array([(point.x, point.y) for point in point_models])

        neigh = NearestNeighbors(n_neighbors=k + 1)
        neigh.fit(data)
        distances, _ = neigh.kneighbors(data)
        k_distances = distances[:, -1]

        sorted_distances = np.sort(k_distances)

        elbow_pt = sorted_distances[-3]

        return elbow_pt

    # def calculate_bi_eps(self, pt_ml_model):
    #     scaler = StandardScaler()
    #     pt_dat_all = PtDat.objects.get(point_model=self)
    #     point_coords = [pt_dat.point_model.coords for pt_dat in pt_dat_all]
    #     point_coords_2 = [pt_dat.point_model.coords for pt_dat in PtDat.objects.get(point_model=pt_ml_model)]
    #
    #     point_coords = point_coords + point_coords_2
    #
    #     scaled = scaler.fit_transform(point_coords)
    #
    #     eps_attempts = [float(j) / 100 for j in range(0, 250, 1)]  # maybe too many?
    #     sh_scores = []
    #
    #     for eps in eps_attempts:
    #         dbscan = DBSCAN(eps=eps, min_samples=5)
    #         labels = dbscan.fit_predict(scaled)
    #         sh_avg = sklearn.metrics.silhouette_score(scaled, labels)
    #         sh_scores.append(sh_avg)
    #
    #     eps = eps_attempts[np.argmax(sh_scores)]
    #
    #     return eps

    @staticmethod
    def cluster_analysis(point_models, eps, min_samples):
        points = []

        for point_model in point_models:
            points.extend(point_model.get_points())

        coordinates = [(point.geometry.x, point.geometry.y) for point in points]

        X = np.array(coordinates)

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X)

        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(points[i])

        return clusters

    # Treat this method as a factory for this model!
    # ________________________________________________________________________________________
    # ____________________________________________██__________________________________________
    # __________________________________________██░░██________________________________________
    # __░░__________░░________________________██░░░░░░██____________________________░░░░______
    # ______________________________________██░░░░░░░░░░██____________________________________
    # ______________________________________██░░░░░░░░░░██____________________________________
    # ____________________________________██░░░░░░░░░░░░░░██__________________________________
    # __________________________________██░░░░░░██████░░░░░░██________________________________
    # __________________________________██░░░░░░██████░░░░░░██________________________________
    # ________________________________██░░░░░░░░██████░░░░░░░░██______________________________
    # ________________________________██░░░░░░░░██████░░░░░░░░██______________________________
    # ______________________________██░░░░░░░░░░██████░░░░░░░░░░██____________________________
    # ____________________________██░░░░░░░░░░░░██████░░░░░░░░░░░░██__________________________
    # ____________________________██░░░░░░░░░░░░██████░░░░░░░░░░░░██__________________________
    # __________________________██░░░░░░░░░░░░░░██████░░░░░░░░░░░░░░██________________________
    # __________________________██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██________________________
    # ________________________██░░░░░░░░░░░░░░░░██████░░░░░░░░░░░░░░░░██______________________
    # ________________________██░░░░░░░░░░░░░░░░██████░░░░░░░░░░░░░░░░██______________________
    # ______________________██░░░░░░░░░░░░░░░░░░██████░░░░░░░░░░░░░░░░░░██____________________
    # ________░░____________██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██____________________
    # ________________________██████████████████████████████████████████______________________
    def get_cluster_geojson(self, clusters):
        features = []

        for cluster_points in clusters.values():
            coordinates = []
            for point in cluster_points:
                coordinates.append(
                    (point.geometry.x,
                     point.geometry.y))  # im not sure about this line, it may or may not be how to access point data
                # coordinates.append((point.latitude, point.longitude))

            convex_hull = Polygon(coordinates)

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [convex_hull.coords[0]],
                },
                "properties": {}
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        filename = f"{uuid.uuid4().hex}.geojson"

        with open(filename, "w") as file:
            json.dump(feature_collection, file)

        self.geogson_file.name = filename
        self.save()

        return self
