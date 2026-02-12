/**
 * Cloud Functions for SmartAgro IoT Application
 * Provides API endpoints for sensor data processing and irrigation predictions
 */

const {onRequest} = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");

// Initialize Firebase Admin
admin.initializeApp();

/**
 * Health check endpoint
 */
exports.healthCheck = onRequest((request, response) => {
  logger.info("Health check requested", {structuredData: true});
  response.json({
    status: "online",
    service: "SmartAgro Cloud Functions",
    timestamp: new Date().toISOString(),
  });
});

/**
 * Get latest sensor data from Realtime Database
 */
exports.getSensorData = onRequest({cors: true}, async (request, response) => {
  try {
    logger.info("Fetching sensor data");

    const db = admin.database();
    const sensorRef = db.ref("/sensor_data");
    const snapshot = await sensorRef.once("value");
    const data = snapshot.val();

    if (data) {
      response.json({
        success: true,
        data: data,
        timestamp: new Date().toISOString(),
      });
    } else {
      response.status(404).json({
        success: false,
        message: "No sensor data found",
      });
    }
  } catch (error) {
    logger.error("Error fetching sensor data:", error);
    response.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

/**
 * Update sensor data in Realtime Database
 */
exports.updateSensorData = onRequest({cors: true}, async (request, response) => {
  try {
    if (request.method !== "POST") {
      response.status(405).json({error: "Method not allowed"});
      return;
    }

    const sensorData = request.body;
    logger.info("Updating sensor data", {data: sensorData});

    const db = admin.database();
    const sensorRef = db.ref("/sensor_data");
    await sensorRef.set({
      ...sensorData,
      timestamp: admin.database.ServerValue.TIMESTAMP,
    });

    response.json({
      success: true,
      message: "Sensor data updated successfully",
    });
  } catch (error) {
    logger.error("Error updating sensor data:", error);
    response.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

/**
 * Get prediction data from Firestore
 */
exports.getPredictions = onRequest({cors: true}, async (request, response) => {
  try {
    logger.info("Fetching predictions from Firestore");

    const db = admin.firestore();
    const fieldDoc = await db.collection("fields").doc("field_1").get();

    if (fieldDoc.exists) {
      response.json({
        success: true,
        data: fieldDoc.data(),
      });
    } else {
      response.status(404).json({
        success: false,
        message: "No predictions found",
      });
    }
  } catch (error) {
    logger.error("Error fetching predictions:", error);
    response.status(500).json({
      success: false,
      error: error.message,
    });
  }
});
