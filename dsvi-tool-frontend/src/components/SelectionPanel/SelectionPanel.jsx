import React from "react";
import { ExpandMore } from "@mui/icons-material";
import {
  FormControlLabel,
  FormControl,
  FormLabel,
  RadioGroup,
  Radio,
  Drawer,
  List,
  ListItem,
  Typography,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Modal,
  Box,
  Icon,
} from "@mui/material";
import { PaidOutlined } from "@mui/icons-material";
import "./SelectionPanel.css";

const drawerWidth = 250;

const SelectionPanel = (props) => {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
    >
      <List>
        <ListItem>
          <Typography>MAIN MENU</Typography>
        </ListItem>
        <Divider />
        <ListItem>
          <FormControl>
            <FormLabel id="admin-level-label">
              Select administrative level
            </FormLabel>
            <RadioGroup
              row
              aria-labelledby="admin-level-label"
              name="admin-level-group"
              value={props.adminLevel}
              onChange={props.changeAdminLevel}
            >
              {["One", "Two", "Three"].map((text, index) => (
                <FormControlLabel
                  sx={{
                    "& .MuiSvgIcon-root": {
                      fontSize: 15,
                    },
                    "& .MuiTypography-root": {
                      fontSize: 15,
                    },
                  }}
                  key={text}
                  value={index + 1}
                  control={<Radio />}
                  label={text}
                />
              ))}
            </RadioGroup>
          </FormControl>
        </ListItem>
        <Divider />
        <ListItem sx={{ padding: 0 }}>
          <Accordion elevation={0}>
            <AccordionSummary
              expandIcon={<ExpandMore />}
              aria-controls="socioeconomic-layers"
              id="socioeconomic-layers-header"
            >
              <PaidOutlined />
              <Typography> Socioeconomic Layers</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl>
                <RadioGroup
                  aria-labelledby="socioeconomic-layers-label"
                  name="socioeconomic-layers-group"
                  value={props.vectorLayer}
                  onChange={props.changeSocioeconomicLayer}
                >
                  {props.vectorLayerList?.map((layer, index) => (
                    <FormControlLabel
                      sx={{
                        "& .MuiSvgIcon-root": {
                          fontSize: 15,
                        },
                        "& .MuiTypography-root": {
                          fontSize: 15,
                        },
                      }}
                      key={layer.name}
                      value={layer.name}
                      control={<Radio />}
                      label={layer.description}
                    />
                  ))}
                </RadioGroup>
              </FormControl>
            </AccordionDetails>
          </Accordion>
        </ListItem>
        <ListItem></ListItem>
      </List>
    </Drawer>
  );
};

export default SelectionPanel;
