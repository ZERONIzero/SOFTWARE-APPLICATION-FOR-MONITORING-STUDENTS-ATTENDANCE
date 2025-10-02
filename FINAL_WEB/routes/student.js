const express = require('express');
const StudentController = require('../controllers/auth');

const router = express.Router();

router.post('/setting',StudentController.make_new_password);
router.get('/setting',(req,res)=>{
    res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name ,});
})

router.get('/',(req,res)=>{
    if (req.session.status == "student" && req.session.name != null) {
        res.render('menu_s',{ login : req.session.login, status : req.session.status, person : req.session.name});
    } else {
        req.session.destroy(function(err) {
            res.redirect("/");
        }) 
    }
})

router.get('/student',(req,res)=>{
    if (req.session.status == "student" && req.session.name != null) {
        res.render('menu_s',{ login : req.session.login, status : req.session.status, person : req.session.name});
    } else {
        req.session.destroy(function(err) {
            res.redirect("/");
        }) 
    }
})

router.get('/schedule',StudentController.get_schedule_of_the_week);
router.post('/schedule',StudentController.update_schedule);

module.exports = router;