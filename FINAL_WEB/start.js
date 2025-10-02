const express = require("express");
const bodyParser=require("body-parser");
const cors = require("cors");
const path = require("path");
const helmet = require('helmet');
const app = express();

const methodOverride = require("method-override");
app.use(methodOverride('_method'));

const session = require("express-session");
app.use(session({
            secret : "VYCaOw5eh0272uvYwP78Mrq0H2aWf-LQUO_Ii-TU",
            resave: true,
            saveUninitialized: true,
            cookie : { 
                httpOnly : true,
                sameSite : 'strict',
                maxAge : 3600000
            }
        }))

// const corsSettings = {
//     origin: 'http://localhost:3000',
//     methods: ['GET', 'POST', 'PUT'],
//     allowedHeaders: ['Content-Type', 'Authorization']
// };

const cookieParser = require("cookie-parser");
app.use(cookieParser("VYCaOw5eh0272uvYwP78Mrq0H2aWf-LQUO_Ii-TU"));

// app.use(cors(corsSettings));

// app.use(helmet({
//     contentSecurityPolicy: {
//         directives: {
//             defaultSrc: ["'self'"],
//             scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'", "cdn.jsdelivr.net"],
//             scriptSrcAttr: ["'unsafe-inline'"],
//             styleSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
//             imgSrc: ["'self'", "data:", "https:"],
//             connectSrc: ["'self'"],
//             fontSrc: ["'self'"],
//             objectSrc: ["'none'"],
//             mediaSrc: ["'self'"],
//             frameSrc: ["'none'"]
//         }
//     },
//     features : {
//         camera: ['none'],
//         geolocation: ['none'],
//     }
// }))

app.use(bodyParser.json());

const publicDirectory = path.join(__dirname,'./style');
app.use(express.static(publicDirectory));

app.use(express.urlencoded({ extended : false }));
app.use(express.json());

app.set('view engine','hbs');

app.listen( 3000 , () => {
    console.log("Сервер запущен");
});

app.use('/',require('./routes/auth'))