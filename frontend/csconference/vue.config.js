// vue.config.js
module.exports = {
    devServer: {
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