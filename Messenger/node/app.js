var express = require("express");
var app = express();
var mysql = require('mysql');

var con = mysql.createConnection
({
	host: "localhost",
	user: "root",
	password: "vasudev123",
	database: "users"
});

con.connect((err) => {
	if (err) throw err;
	console.log("Connected")
})

var bodyParser = require('body-parser');
app.use (bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));
app.listen(3000, () => {
 console.log("Server running on port 3000");
});
app.post("/register", (req, res) => {
 var username = req.body.username;
 console.log(req.body.hashed_password)
 var password = req.body.hashed_password;
 console.log(username)
 var salt = req.body.salt;
 console.log(salt)
 console.log(password)
 var sql =	`INSERT INTO user (username, hashed_password, salt) VALUES ('${username}', '${password}', '${salt}' );`
 console.log(sql)

 con.query(sql, function (err, result) {
	 if (err) throw err;
	 console.log("Inserted register")
 });
 
 
 
 //res.json(["Tony","Lisa","Michael","Ginger","Food"]);
 
});

app.post("/login", (req, res) => {
 var username = req.body.username;
 var password = req.body.password;
 
 var sql =	`SELECT * FROM user WHERE username='${username}';`

 con.query(sql, function (err, result) {
	 if (err) throw err;
	 //console.log(result.hashed_password.toString())
	 console.log(result)
	 user = result[0]
	 user.hashed_password = user.hashed_password.toString()
	 user.salt = user.salt.toString()
	 res.json(user)
	 console.log("login")
	 res.end()
 });
 
 
 
 //res.json(["Tony","Lisa","Michael","Ginger","Food"]);
 
});

