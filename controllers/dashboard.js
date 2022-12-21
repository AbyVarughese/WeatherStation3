"use strict";

const accounts = require("./accounts.js");
const logger = require("../utils/logger");
const stationStore = require("../models/station-store");
const uuid = require("uuid");
const headerHelper = require("../utils/headerHelper");


const dashboard = {
  index(request, response) {
    logger.info("dashboard rendering");
    const loggedInUser = accounts.getCurrentUser(request);
    const stations = stationStore.getUserStations(loggedInUser.id);
    stations.sort((a,b) => {
      return a.title.localeCompare(b.title);
    });
    for (let i = 0; i < stations.length; i++) {
      stations[i].header = headerHelper.getHeader(stations[i]);
       }
    let markers = "";
    for (let i = 0; i < stations.length; i++) {
      markers += "L.marker(["+stations[i].latitude.toString()+", "+stations[i].longitude.toString()+"]).addTo(map);\r\n";
    }
    let mapview = null;
    if (stations.length > 0) {
    mapview = ".setView(["+stations[0].latitude.toString()+", "+stations[0].longitude.toString()+"], 6.4)";
    }
    const viewData = {
      title: "Weather top Dashboard",
      stations: stations,
      account: loggedInUser,
      markers: markers,
      mapview: mapview,
    };
    logger.info("about to render", stations);
    response.render("dashboard", viewData);
  },
  async addreport(request, response) {
    logger.info("rendering new report");
    let report = {};
    const lat = request.body.lat;
    const lng = request.body.lng;
    const requestUrl = `https://api.openweathermap.org/data/2.5/onecall?lat=${lat}&lon=${lng}&units=metric&appid=YOUR_API_KEY_HERE`
    const result = await axios.get(requestUrl);
    if (result.status == 200) {
      const reading = result.data.current;
      report.code = reading.weather[0].id;
      report.temperature = reading.temp;
      report.windSpeed = reading.wind_speed;
      report.pressure = reading.pressure;
      report.windDirection = reading.wind_dir;
    }
    console.log(report);
    const viewData = {
      title: "Weather Report",
      reading: report
    };
    response.render("dashboard", viewData);
  },
  deleteStation(request, response) {
    const stationId = request.params.id;
    logger.debug(`Deleting Station ${stationId}`);
    stationStore.removeStation(stationId);
    response.redirect("/dashboard");
  },

  addStation(request, response) {
    const loggedInUser = accounts.getCurrentUser(request);
    if(request.body.title.length == 0 || request.body.latitude.length == 0 || request.body.longitude.length == 0) {
      logger.warn("Invalid values");
    }else {
    const newStation = {
      id: uuid.v1(),
      userid: loggedInUser.id,
      title: request.body.title,
      latitude: request.body.latitude,
      longitude: request.body.longitude,
      readings: []
    };
    logger.debug("Creating a new Station", newStation);
    stationStore.addStation(newStation);
  }
    response.redirect("/dashboard");
  }
};

module.exports = dashboard;
