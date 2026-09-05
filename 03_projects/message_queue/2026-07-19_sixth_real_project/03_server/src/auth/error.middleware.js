
export function errorHandler(err, req, res, next) {
  const status = err.status || 500

  res.status(status).json({
    success: false,
    message: err.message || "server error",
    data: err.data || {}
  })
}