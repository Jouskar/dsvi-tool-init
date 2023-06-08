import { useState } from "react";

export const BASE_URL = "http://127.0.0.1:8000/";

export const endpoints = {
  login: "login",
  vector: "vector",
  layerTypes: "layer-types",
  vectorAnalyze: "vector-ml",
};

const objectToQuerystring = (obj) => {
  if (obj) {
    let queryString = "?";
    for (let key of Object.keys(obj)) {
      if (obj[key] !== "") {
        if (queryString !== "?") queryString += "&";
        queryString += key + "=" + encodeURIComponent(obj[key]);
      }
    }
    return queryString === "?" ? "" : queryString;
  } else {
    return "";
  }
};

const useHttp = (requestConfig, applyData) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [reqBody, setReqBody] = useState(null);

  const sendRequest = async () => {
    setIsLoading(true);
    setError(null);

    try {
      console.log("req", requestConfig);
      const response = await fetch(
        `${BASE_URL}${requestConfig.endpoint}${objectToQuerystring(
          requestConfig.query
        )}`,
        {
          mode: "cors",
          method: requestConfig.method,
          headers: requestConfig.headers,
          body: reqBody !== null ? reqBody : JSON.stringify(requestConfig.body),
        }
      );

      if (!response.ok) throw new Error("Request failed!");

      const data = await response.json();

      applyData(data);
    } catch (error) {
      setError(error.message || "Something went wrong!");
      console.log(error);
    }
    setIsLoading(false);
  };

  return {
    isLoading,
    error,
    sendRequest,
    setReqBody,
  };
};

export default useHttp;
