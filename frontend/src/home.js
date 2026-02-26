import { useState, useEffect } from "react";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import React from "react";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import {
  Paper,
  CardActionArea,
  CardMedia,
  Grid,
  TableContainer,
  Table,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
  Button,
  CircularProgress,
  Chip,
  Divider,
} from "@material-ui/core";
import image from "./bg.png";
import { DropzoneArea } from "material-ui-dropzone";
import { common } from "@material-ui/core/colors";
import Clear from "@material-ui/icons/Clear";

const ColorButton = withStyles((theme) => ({
  root: {
    color: "#fff",
    backgroundColor: "#2e7d32",
    "&:hover": {
      backgroundColor: "#1b5e20",
    },
  },
}))(Button);
const axios = require("axios").default;

const useStyles = makeStyles((theme) => ({
  grow: {
    flexGrow: 1,
  },
  clearButton: {
    width: "-webkit-fill-available",
    borderRadius: "12px",
    padding: "12px 22px",
    color: "#fff",
    fontSize: "16px",
    fontWeight: 700,
    letterSpacing: "0.5px",
  },
  root: {
    maxWidth: 345,
    flexGrow: 1,
  },
  media: {
    height: 400,
  },
  paper: {
    padding: theme.spacing(2),
    margin: "auto",
    maxWidth: 500,
  },
  gridContainer: {
    justifyContent: "center",
    padding: "3em 1em 2em 1em",
  },
  mainContainer: {
    backgroundImage: `url(${image})`,
    backgroundRepeat: "no-repeat",
    backgroundPosition: "center",
    backgroundSize: "cover",
    minHeight: "93vh",
    marginTop: "0px",
  },
  imageCard: {
    margin: "auto",
    maxWidth: 420,
    minHeight: 480,
    backgroundColor: "rgba(255,255,255,0.97)",
    boxShadow: "0px 12px 40px 0px rgba(0,0,0,0.25) !important",
    borderRadius: "16px",
    overflow: "visible",
  },
  imageCardEmpty: {
    minHeight: "auto",
  },
  noImage: {
    margin: "auto",
    width: 400,
    height: "400 !important",
  },
  input: {
    display: "none",
  },
  uploadIcon: {
    background: "white",
  },
  tableContainer: {
    backgroundColor: "transparent !important",
    boxShadow: "none !important",
  },
  table: {
    backgroundColor: "transparent !important",
  },
  tableHead: {
    backgroundColor: "transparent !important",
  },
  tableRow: {
    backgroundColor: "transparent !important",
  },
  tableCell: {
    fontSize: "20px",
    backgroundColor: "transparent !important",
    borderColor: "transparent !important",
    color: "#1a1a1a !important",
    fontWeight: "bold",
    padding: "4px 16px",
  },
  tableCell1: {
    fontSize: "13px",
    backgroundColor: "transparent !important",
    borderColor: "transparent !important",
    color: "#666 !important",
    fontWeight: "600",
    padding: "4px 16px",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  tableBody: {
    backgroundColor: "transparent !important",
  },
  text: {
    color: "white !important",
    textAlign: "center",
  },
  buttonGrid: {
    maxWidth: "436px",
    width: "100%",
  },
  detail: {
    backgroundColor: "white",
    display: "flex",
    justifyContent: "center",
    flexDirection: "column",
    alignItems: "stretch",
    padding: "16px !important",
  },
  appbar: {
    background: "linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%)",
    boxShadow: "0 2px 12px rgba(0,0,0,0.15)",
    color: "white",
  },
  loader: {
    color: "#2e7d32 !important",
  },
  // ── New styles for expanded info ──
  sectionTitle: {
    fontSize: "14px",
    fontWeight: 700,
    color: "#2e7d32",
    marginTop: "12px",
    marginBottom: "6px",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  infoList: {
    margin: "0",
    paddingLeft: "18px",
    "& li": {
      fontSize: "13px",
      color: "#444",
      marginBottom: "4px",
      lineHeight: 1.5,
    },
  },
  severityChip: {
    fontWeight: 700,
    fontSize: "12px",
    marginLeft: "8px",
  },
  divider: {
    margin: "10px 0",
    backgroundColor: "#e0e0e0",
  },
  warningBox: {
    padding: "16px",
    textAlign: "center",
    borderRadius: "12px",
    backgroundColor: "#fff3e0",
    border: "1px solid #ffe0b2",
  },
  brandText: {
    fontWeight: 700,
    fontSize: "18px",
    letterSpacing: "1px",
  },
  brandSub: {
    fontSize: "12px",
    opacity: 0.85,
    marginLeft: "8px",
    fontWeight: 400,
  },
}));

// ── Helper: severity color ──
const getSeverityColor = (severity) => {
  if (!severity) return "#999";
  const s = severity.toLowerCase();
  if (s.includes("severe")) return "#d32f2f";
  if (s.includes("moderate")) return "#f57c00";
  if (s.includes("none") || s.includes("healthy")) return "#2e7d32";
  return "#1976d2";
};

export const ImageUpload = () => {
  const classes = useStyles();
  const [selectedFile, setSelectedFile] = useState();
  const [preview, setPreview] = useState();
  const [data, setData] = useState();
  const [image, setImage] = useState(false);
  const [isLoading, setIsloading] = useState(false);
  let confidence = 0;

  const sendFile = async () => {
    if (image) {
      try {
        let formData = new FormData();
        formData.append("file", selectedFile);
        let res = await axios({
          method: "post",
          url: process.env.REACT_APP_API_URL,
          data: formData,
        });
        if (res.status === 200) {
          setData(res.data);
        }
      } catch (error) {
        console.error("Prediction failed:", error);
        setData({ disease_class: "Error", confidence: 0, error: true });
      }
      setIsloading(false);
    }
  };

  const clearData = () => {
    setData(null);
    setImage(false);
    setSelectedFile(null);
    setPreview(null);
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    if (!preview) {
      return;
    }
    setIsloading(true);
    sendFile();
  }, [preview]); // eslint-disable-line react-hooks/exhaustive-deps

  const onSelectFile = (files) => {
    if (!files || files.length === 0) {
      setSelectedFile(undefined);
      setImage(false);
      setData(undefined);
      return;
    }
    setSelectedFile(files[0]);
    setData(undefined);
    setImage(true);
  };

  if (data) {
    confidence = parseFloat(data.confidence).toFixed(2);
  }

  return (
    <React.Fragment>
      <AppBar position="static" className={classes.appbar}>
        <Toolbar>
          <Typography className={classes.brandText} variant="h6" noWrap>
            🌿 LeafLens
            <span className={classes.brandSub}>by @Maharsh Doshi</span>
          </Typography>
          <div className={classes.grow} />
          <Typography variant="caption" style={{ opacity: 0.7 }}>
            Potato Disease Detection AI
          </Typography>
        </Toolbar>
      </AppBar>
      <Container
        maxWidth={false}
        className={classes.mainContainer}
        disableGutters={true}
      >
        <Grid
          className={classes.gridContainer}
          container
          direction="row"
          justifyContent="center"
          alignItems="center"
          spacing={2}
        >
          <Grid item xs={12}>
            <Card
              className={`${classes.imageCard} ${!image ? classes.imageCardEmpty : ""
                }`}
            >
              {image && (
                <CardActionArea>
                  <CardMedia
                    className={classes.media}
                    image={preview}
                    component="image"
                    title="Uploaded leaf image"
                    style={{ borderRadius: "16px 16px 0 0" }}
                  />
                </CardActionArea>
              )}
              {!image && (
                <CardContent className={classes.content}>
                  <DropzoneArea
                    acceptedFiles={["image/*"]}
                    dropzoneText={
                      "Drag and drop an image of a potato leaf to analyze"
                    }
                    onChange={onSelectFile}
                  />
                </CardContent>
              )}

              {/* ── NOT A LEAF WARNING ── */}
              {data && data.is_leaf === false && (
                <CardContent className={classes.detail}>
                  <div className={classes.warningBox}>
                    <Typography
                      variant="h6"
                      style={{
                        color: "#e65100",
                        fontWeight: "bold",
                        marginBottom: 8,
                      }}
                    >
                      ⚠️ Not a Plant Leaf
                    </Typography>
                    <Typography variant="body2" style={{ color: "#795548" }}>
                      {data.validation_message ||
                        "Please upload an image of a potato plant leaf for disease detection."}
                    </Typography>
                  </div>
                </CardContent>
              )}

              {/* ── PREDICTION RESULTS ── */}
              {data && data.is_leaf !== false && (
                <CardContent className={classes.detail}>
                  {/* Disease & Confidence */}
                  <TableContainer
                    component={Paper}
                    className={classes.tableContainer}
                  >
                    <Table
                      className={classes.table}
                      size="small"
                      aria-label="results"
                    >
                      <TableHead className={classes.tableHead}>
                        <TableRow className={classes.tableRow}>
                          <TableCell className={classes.tableCell1}>
                            Disease Detected
                          </TableCell>
                          <TableCell
                            align="right"
                            className={classes.tableCell1}
                          >
                            Confidence
                          </TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody className={classes.tableBody}>
                        <TableRow className={classes.tableRow}>
                          <TableCell
                            component="th"
                            scope="row"
                            className={classes.tableCell}
                          >
                            {data.disease_class || data.class}
                            {data.treatment_info && data.treatment_info.severity && (
                              <Chip
                                label={data.treatment_info.severity}
                                size="small"
                                className={classes.severityChip}
                                style={{
                                  backgroundColor: getSeverityColor(
                                    data.treatment_info.severity
                                  ),
                                  color: "#fff",
                                }}
                              />
                            )}
                          </TableCell>
                          <TableCell
                            align="right"
                            className={classes.tableCell}
                          >
                            {confidence}%
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>

                  {/* ── Detailed Treatment Info ── */}
                  {data.treatment_info && (
                    <div style={{ padding: "0 8px" }}>
                      {/* Symptoms */}
                      {data.treatment_info.symptoms &&
                        data.treatment_info.symptoms.length > 0 && (
                          <>
                            <Divider className={classes.divider} />
                            <Typography className={classes.sectionTitle}>
                              🔍 Symptoms
                            </Typography>
                            <ul className={classes.infoList}>
                              {data.treatment_info.symptoms.map((s, i) => (
                                <li key={i}>{s}</li>
                              ))}
                            </ul>
                          </>
                        )}

                      {/* Causes */}
                      {data.treatment_info.causes &&
                        data.treatment_info.causes.length > 0 && (
                          <>
                            <Divider className={classes.divider} />
                            <Typography className={classes.sectionTitle}>
                              🧬 Causes
                            </Typography>
                            <ul className={classes.infoList}>
                              {data.treatment_info.causes.map((c, i) => (
                                <li key={i}>{c}</li>
                              ))}
                            </ul>
                          </>
                        )}

                      {/* Treatment */}
                      {data.treatment_info.treatment &&
                        data.treatment_info.treatment.length > 0 && (
                          <>
                            <Divider className={classes.divider} />
                            <Typography className={classes.sectionTitle}>
                              💊 Treatment
                            </Typography>
                            <ul className={classes.infoList}>
                              {data.treatment_info.treatment.map((t, i) => (
                                <li key={i}>{t}</li>
                              ))}
                            </ul>
                          </>
                        )}

                      {/* Prevention */}
                      {data.treatment_info.prevention &&
                        data.treatment_info.prevention.length > 0 && (
                          <>
                            <Divider className={classes.divider} />
                            <Typography className={classes.sectionTitle}>
                              🛡️ Prevention
                            </Typography>
                            <ul className={classes.infoList}>
                              {data.treatment_info.prevention.map((p, i) => (
                                <li key={i}>{p}</li>
                              ))}
                            </ul>
                          </>
                        )}

                      {/* Scientific Name */}
                      {data.treatment_info.scientific_name && (
                        <>
                          <Divider className={classes.divider} />
                          <Typography
                            variant="caption"
                            style={{
                              color: "#999",
                              fontStyle: "italic",
                              display: "block",
                              textAlign: "center",
                              marginTop: "4px",
                            }}
                          >
                            Scientific name:{" "}
                            {data.treatment_info.scientific_name}
                          </Typography>
                        </>
                      )}
                    </div>
                  )}
                </CardContent>
              )}

              {isLoading && (
                <CardContent className={classes.detail}>
                  <div style={{ textAlign: "center", padding: "20px" }}>
                    <CircularProgress
                      color="secondary"
                      className={classes.loader}
                    />
                    <Typography
                      variant="body2"
                      style={{ marginTop: 10, color: "#666" }}
                    >
                      Analyzing leaf image...
                    </Typography>
                  </div>
                </CardContent>
              )}
            </Card>
          </Grid>
          {data && (
            <Grid item className={classes.buttonGrid}>
              <ColorButton
                variant="contained"
                className={classes.clearButton}
                color="primary"
                component="span"
                size="large"
                onClick={clearData}
                startIcon={<Clear fontSize="large" />}
              >
                Clear & Scan Another
              </ColorButton>
            </Grid>
          )}
        </Grid>
      </Container>
    </React.Fragment>
  );
};
