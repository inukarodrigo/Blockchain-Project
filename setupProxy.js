const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/get_wallet_details",
    createProxyMiddleware({
      target: "http://localhost:5000", // Replace with the correct Flask server address
      changeOrigin: true,
    })
  );
};

