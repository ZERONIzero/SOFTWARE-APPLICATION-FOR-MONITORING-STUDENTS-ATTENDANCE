const express = require('express');
const authController = require('../controllers/auth') 
const studentRoutes = require('./student');
const teacherRoutes = require('./teacher');

const router = express.Router();

router.post('/', authController.log_in_to_the_system)
router.post('/authorization', authController.log_in_to_the_system)

router.get('/',(req,res)=>{
    console.log(req.session)
    if (req.session.login == null){
        res.render("authorization", { title: "Sign in"})
    } else if (req.session.login != null && req.session.status === "student"){
        res.redirect("menu");
    } else {
        res.redirect("menu");
    }
})

router.get('/authorization', (req,res)=>{
    console.log(req.session)
    if (req.session.login == null){
        res.render("authorization", { title: "Sign in"})
    } else if (req.session.login != null && req.session.status === "student"){
        res.redirect("menu");
    } else {
        res.redirect("menu");
    }
})

router.get('/menu',(req,res)=>{
    if (req.session.login == null){
        res.redirect("/");
    } else {
        if (req.session.status == "student" && req.session.name != null) {
            res.redirect('/student');
        }
        else {
            res.redirect('/teacher');
        }
    }
})

router.get('/reset_password',authController.reset)
router.post('/reset_password',authController.edit)

router.use('/student', studentRoutes);
router.use('/teacher', teacherRoutes);

router.get('/logout',(req,res)=>{
    req.session.destroy(function(err) {
        res.redirect("/");
    })    
})

module.exports = router;

