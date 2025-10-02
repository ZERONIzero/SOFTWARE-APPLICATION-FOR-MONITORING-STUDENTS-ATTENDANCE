const express = require('express');
const TeacherController = require('../controllers/auth');

const router = express.Router();

router.get('/',(req,res)=>{
    if (req.session.status == "teacher" && req.session.name != null) {
        res.render('menu_t',{ login : req.session.login, status : req.session.status, person : req.session.name})
    } else {
        req.session.destroy(function(err) {
            res.redirect("/");
        }) 
    }
})

router.post('/setting', TeacherController.make_new_password);
router.get('/setting',(req,res)=>{
    res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name });
})

router.get('/teacher',(req,res)=>{
    if (req.session.status == "teacher" && req.session.name != null) {
        res.render('menu_t',{ login : req.session.login, status : req.session.status, person : req.session.name});
    } else {
        req.session.destroy(function(err) {
            res.redirect("/");
        }) 
    }
})

router.get('/schedule',TeacherController.get_schedule_of_the_week);
router.post('/schedule',TeacherController.update_schedule);

router.get('/change_audience', (req,res)=>{ res.render('change_a');});
router.put('/change_audience',TeacherController.select_schedule);
router.post('/change_audience',TeacherController.change_schedule_room)

router.get('/mark_a_student', TeacherController.get_group_list);
router.put('/mark_a_student', TeacherController.get_schedule_and_student);
router.post('/mark_a_student', TeacherController.mark_a_student);

module.exports = router;

