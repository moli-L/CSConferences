var express = require('express');
var bodyParser = require('body-parser');
var mysql = require('mysql');

var app = express();
// parse application/json
app.use(bodyParser.json());
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({
    extended: true
}));

var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'csconferences',
    port: 3306
});
connection.connect();

app.get('/', function (req, res) {
    res.send('Hello World');
})
app.post('/', function (req, res) {
    res.send('Hello World');
})

app.get('/sql', function (req, res) {
    console.log('A client request');
    res.send('Use POST');
})
app.post('/sql', function (req, res) {
    console.log('A client post');
    console.log(req.body);
    msql = req.body.sql;
    doQuery(msql).then(data => {
        if(data) {
            data = data.map(item => {
                if(item['s_date']) 
                    item['s_date'] = item['s_date'].toLocaleDateString()
                if(item['e_date'])
                    item['e_date'] = item['e_date'].toLocaleDateString()
                if(item['paper_date'])
                    item['paper_date'] = item['paper_date'].toLocaleDateString()
                if(item['noti_date'])
                    item['noti_date'] = item['noti_date'].toLocaleDateString()
                
                return item
            })
        }
        res.json({err:false, msg:'success', data: data})
    }, (err) => {
        res.json({err:true, msg:'fail', data: null})
    })
})

function doQuery(msql) {
    return new Promise((resolve, reject) => {
        connection.query(msql, (err, result) => {
            if (err) {
                console.log('[SELECT ERROR] - ', err.message);
                reject({err:true});
                return;
            }
            console.log('--------------------------SELECT----------------------------');
            // console.log(result);
            resolve(result);
            console.log('------------------------------------------------------------\n\n');
        });
    })
}

var server = app.listen(8088, function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log(`应用实例，访问地址为 http://localhost:${port}`);
})