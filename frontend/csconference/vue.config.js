// vue.config.js
module.exports = {
    devServer: {
        open: true,
        host: 'localhost',
        port: 8080,
        proxy: {
            'api': {
                target: 'http://localhost:8088/',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
}