const mysql = require("mysql2");
const nodemailer = require("nodemailer");

const config = require("../tool/db");
const config_mail = require("../tool/mail");

const bcrypt = require("bcryptjs");

const hbs = require("hbs");

const methodOverride = require("method-override");

let transporter = nodemailer.createTransport({
    pool: true,
    host: config_mail.host,
    port: config_mail.port,
    secure: config_mail.secure,
    auth: {
        user: config_mail.auth.user,
        pass: config_mail.auth.pass,
    }
});

let con = mysql.createConnection({
    host: config.hostname,
    user: config.username,
    password: config.password,
    database: config.database,
    port: config.port,
});

async function sendMail(code,email) {

    let message = {
        from: "ERRORZERONI@yandex.ru",
        to: email,
        subject: 'Reset password message',
        text: "Dear user, I send secure password ("+code+")",
    }

    await transporter.sendMail(message);
};

function check(put,out) {
    return(bcrypt.compareSync(put,out));
}

let test_code = '';
let reset_title = '';


exports.log_in_to_the_system = async (req, res)=>{
    try {
        const { Email_address, Password } = req.body;

        if (!Email_address || Email_address === '') {
            return res.render('authorization', {
                message: 'Login empty'
            });
        }

        if (!Password || Password === '') {
            return res.render('authorization', {
                message: 'Password empty'
            });
        }

        const teacherResults = await new Promise((resolve, reject) => {
            con.query(
                'SELECT password, login, last_name, first_name, middle_name FROM `Teacher` WHERE login = ?', 
                [Email_address],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        });

        if (teacherResults.length > 0) {
            if (check(Password, teacherResults[0].password)) {
                req.session.login = teacherResults[0].login;
                req.session.status = "teacher";
                req.session.name = `${teacherResults[0].last_name} ${teacherResults[0].first_name} ${teacherResults[0].middle_name}`;
                return res.redirect("menu");
            } else {
                req.session.login = Email_address;
                return res.render('authorization', {
                    message: ' ',
                    reset: 'Incorrect password'
                });
            }
        }

        const studentResults = await new Promise((resolve, reject) => {
            con.query(
                'SELECT password, login, last_name, first_name, middle_name FROM `Student` WHERE login = ?',
                [Email_address],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        });

        if (studentResults.length > 0) {
            if (check(Password, studentResults[0].password)) {
                req.session.login = studentResults[0].login;
                req.session.status = "student";
                req.session.name = `${studentResults[0].last_name} ${studentResults[0].first_name} ${studentResults[0].middle_name}`;
                return res.redirect("menu");
            } else {
                req.session.login = Email_address;
                return res.render('authorization', {
                    message: 'Incorrect',
                    reset: 'password'
                });
            }
        }

        return res.render('authorization', {
            message: 'User not found'
        });

    } catch (error) {
        console.error('Login error:', error);
        return res.render('authorization', {
            message: 'Server error occurred'
        });
    }
};

exports.make_new_password = async (req, res)=> {
    const { pass , r_pass } = req.body;

    con.query('SELECT last_name,first_name,middle_name,password FROM `Student` WHERE email = ? AND login = ? LIMIT 1', [pass,req.session.login], async (error,results) => {
        if (error) {
            return console.log(error);
        } else if (!results.length) { 
            return res.render('setting',{
                login : req.session.login,
                status : req.session.status,
                person : req.session.name,
                message : "Пользователь не найден с таким email"
            });                                                  
        }
        if (results < 1){
            return res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name, message : "Пользователь не найден с таким email"});
        } else {
            if (check(r_pass, results[0].password)){
                let name = String(results[0].last_name)+" "+String(results[0].first_name)+" "+String(results[0].middle_name);
                if (req.session.name === name){
                    let test_code="";
                    let chars = 'acdefhiklmnoqrstuvwxyz0123456789'.split('');
                    for(let i=0; i<15; i++){
                        let x = Math.floor(Math.random() * chars.length);
                        test_code += chars[x];
                    }
                    sendMail(test_code,pass);
                    let hashedPassword_new = await bcrypt.hash(test_code,10);
                    con.query('UPDATE `Student` SET password = ? WHERE email = ? AND login = ? LIMIT 1' , [hashedPassword_new, pass, req.session.login], async (error,results)=>{
                        if (error)
                        {
                            return res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name, message : "password not update"});
                        }
                        else {
                            return res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name, message : "password update"});
                        }
                    })
                } else {
                    return res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name, message : "Вы не тот человек"});
                }
            } else {
                return res.render('setting',{login : req.session.login, status : req.session.status, person : req.session.name, message : "Пароли не совпадают"});
            }
        }
    }); 
}

exports.update_schedule = async (req, res)=> {
    const { week_date_select } = req.body;

    let formattedWeekDates;
    let group_code;
    let mas_schedule = [];

    if (req.session.status === "student"){
        mas_schedule = Array.from({ length: 6 }, () => 
            Array.from({ length: 6 }, (_, index) => ({ number_pair: index + 1, name: '', room: '' }))
        );
    } else {
        mas_schedule = Array.from({ length: 6 }, () => 
            Array.from({ length: 6 }, (_, index) => ({ number_pair: index + 1, name: '', room: '' , stud_list: ''}))
        );
    }

    con.query('SELECT start_pair,end_pair FROM `Timepair`', async (error,results) => {
        if (error) {
            return console.log(error);
        } else if (!results.length) { 
            return res.render('',{
                login : req.session.login,
                status : req.session.status,
                person : req.session.name
            });                                                  
        }

        let pair=[];
        for (let i=0;i<results.length;i++){
            pair[i]=String(results[i].start_pair).slice(0,-3)+"-"+String(results[i].end_pair).slice(0,-3);
        }
        

        let mondayDate = new Date(week_date_select);
        let weekDates = [];
        for (let i = 0; i < 6; i++) {
            const date = new Date(mondayDate);
            date.setDate(mondayDate.getDate() + i);
            weekDates.push(date);
        }

        formattedWeekDates = weekDates.map(date => {
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            return `${year}-${month}-${day}`;
        });

        if (req.session.status === "student") {
            con.query('SELECT group_code FROM `Students_in_group` WHERE student_code = (SELECT id FROM `Student` WHERE login = ? LIMIT 1) LIMIT 1',[req.session.login], async(error,results)=> {
                if (error) {
                    return console.log(error);
                } else if (!results.length) { 
                    return res.render('',{
                        login : req.session.login,
                        status : req.session.status,
                        person : req.session.name
                    });                                                  
                }
                group_code = String(results[0].group_code);
                const schedulePromises = formattedWeekDates.map((date_select, j) => {
                    return new Promise((resolve, reject) => {
                        con.query('SELECT `Schedule`.number_pair, `Subject`.name, `Schedule`.room FROM `Schedule` LEFT JOIN `Subject` ON `Schedule`.subject = `Subject`.id WHERE `Schedule`.group = ? AND `Schedule`.date = ?',[group_code, date_select], (error, results) => {
                            if (error) {
                                return reject(error);
                            } else if (!results.length) {
                                return resolve([]);
                            }

                            let scheduleForDay = [];
                            scheduleForDay.length = 6;
                            scheduleForDay = scheduleForDay.fill(0).map((_,index) => ({ number_pair: index+1 , name: '', room: '' }));

                            if (results.length) {
                                results.forEach((item) => {
                                    scheduleForDay[item.number_pair - 1] = {
                                        number_pair: item.number_pair,
                                        name: item.name || '',
                                        room: item.room || ''
                                    };
                                });
                            }
                            mas_schedule[j] = scheduleForDay; 
                            resolve();
                        });
                    });
                });
                try {
                    await Promise.all(schedulePromises);
                    return res.render('schedule', { pair: pair, schedule: mas_schedule , dates: formattedWeekDates});
                } catch (error) {
                    console.log(error);
                    return res.status(500).send('Error fetching schedule');
                }
            });
        } else if (req.session.status === "teacher" ) {
            const [last_name, first_name] = req.session.name.split(" ");
            con.query('SELECT id FROM `Teacher` WHERE login = ? AND first_name = ? AND last_name = ? LIMIT 1',[req.session.login,first_name,last_name], async(error,results)=> {
                if (error) {
                    return console.log(error);
                } else if (!results.length) { 
                    return res.render('',{
                        login : req.session.login,
                        status : req.session.status,
                        person : req.session.name
                    });                                                  
                }
                const teacher_id = String(results[0].id);
                const schedulePromises = formattedWeekDates.map((date_select, j) => {
                    return new Promise((resolve, reject) => {
                        con.query('SELECT `Schedule`.number_pair, `Subject`.name, `Schedule`.room, (SELECT GROUP_CONCAT(CONCAT(`Student`.first_name," ",`Student`.last_name) SEPARATOR ", ") FROM `Student` WHERE `Student`.id IN ( SELECT `Attendance`.student_id FROM `Attendance` WHERE `Attendance`.schedule_id = `Schedule`.id )) AS student_fl FROM `Schedule` LEFT JOIN `Subject` ON `Schedule`.subject = `Subject`.id WHERE `Schedule`.teacher = ? AND `Schedule`.date = ?',
                            [teacher_id, date_select], (error, results) => {
                            if (error) {
                                return reject(error);
                            } else if (!results.length) {
                                return resolve([]);
                            }

                            let scheduleForDay = [];
                            scheduleForDay.length = 6;
                            scheduleForDay = scheduleForDay.fill(0).map((_,index) => ({ number_pair: index+1 , name: '', room: '' , stud_list: ''}));

                            if (results.length) {
                                results.forEach((item) => {
                                    scheduleForDay[item.number_pair - 1] = {
                                        number_pair: item.number_pair,
                                        name: item.name || '',
                                        room: item.room || '',
                                        stud_list : item.student_fl || '',
                                    };
                                });
                            }
                            mas_schedule[j] = scheduleForDay; 
                            resolve();
                        });
                    });
                });
                try {
                    await Promise.all(schedulePromises);
                    return res.render('schedule', { pair: pair, schedule: mas_schedule , dates: formattedWeekDates});
                } catch (error) {
                    console.log(error);
                    return res.status(500).send('Error fetching schedule');
                }
            });
        }
    });
}

exports.get_schedule_of_the_week = async (req, res) => {
    let formattedWeekDates;
    let mas_schedule = [];

    if (req.session.status === "student"){
        mas_schedule = Array.from({ length: 6 }, () => 
            Array.from({ length: 6 }, (_, index) => ({ number_pair: index + 1, name: '', room: '' }))
        );
    } else {
        mas_schedule = Array.from({ length: 6 }, () => 
            Array.from({ length: 6 }, (_, index) => ({ number_pair: index + 1, name: '', room: '' , stud_list: '', group: ''}))
        );
    }

    try {
        const pairResults = await new Promise((resolve, reject) => {
            con.query('SELECT start_pair,end_pair FROM `Timepair`', (error, results) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(results);
            });
        });

        let pair = pairResults.map(item => 
            `${String(item.start_pair).slice(0,-3)}-${String(item.end_pair).slice(0,-3)}`
        );

        let currentDate = new Date();
        let currentDayOfWeek = currentDate.getDay();
        let mondayDate = new Date(currentDate);
        mondayDate.setDate(currentDate.getDate() - (currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1));

        let weekDates = [];
        for (let i = 0; i < 6; i++) {
            const date = new Date(mondayDate);
            date.setDate(mondayDate.getDate() + i);
            weekDates.push(date);
        }

        formattedWeekDates = weekDates.map(date => {
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            return `${year}-${month}-${day}`;
        });

        if (req.session.status === "student") {
            const groupResults = await new Promise((resolve, reject) => {
                con.query('SELECT group_code FROM `Students_in_group` WHERE student_code = (SELECT id FROM `Student` WHERE login = ? LIMIT 1) LIMIT 1',
                    [req.session.login],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            });

            if (!groupResults || !groupResults.length) {
                throw new Error('Group not found');
            }

            const group_code = groupResults[0].group_code;

            const schedulePromises = formattedWeekDates.map((date_select, j) => {
                return new Promise((resolve, reject) => {
                    con.query('SELECT `Schedule`.number_pair, `Subject`.name, `Schedule`.room FROM `Schedule` LEFT JOIN `Subject` ON `Schedule`.subject = `Subject`.id WHERE `Schedule`.group = ? AND `Schedule`.date = ?',
                        [group_code, date_select],
                        (error, results) => {
                            if (error) reject(error);
                            else resolve({ results, dayIndex: j });
                        }
                    );
                });
            });

            const scheduleResults = await Promise.all(schedulePromises);
            scheduleResults.forEach(({ results, dayIndex }) => {
                if (results.length) {
                    results.forEach(item => {
                        mas_schedule[dayIndex][item.number_pair - 1] = {
                            number_pair: item.number_pair,
                            name: item.name || '',
                            room: item.room || ''
                        };
                    });
                }
            });

        } else if (req.session.status === "teacher") {
            const [last_name, first_name, middle_name] = req.session.name.split(" ");
            const teacherResults = await new Promise((resolve, reject) => {
                con.query('SELECT id FROM `Teacher` WHERE login = ? AND first_name = ? AND last_name = ? LIMIT 1',
                    [req.session.login, first_name, last_name],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            });

            if (!teacherResults || !teacherResults.length) {
                throw new Error('Teacher not found');
            }

            const teacher_id = teacherResults[0].id;
            const schedulePromises = formattedWeekDates.map((date_select, j) => {
                return new Promise((resolve, reject) => {
                    con.query('SELECT `Schedule`.number_pair, `Subject`.name, `Schedule`.room, (SELECT GROUP_CONCAT(CONCAT(`Student`.first_name," ",`Student`.last_name) SEPARATOR ", ") FROM `Student` WHERE `Student`.id IN ( SELECT `Attendance`.student_id FROM `Attendance` WHERE `Attendance`.schedule_id = `Schedule`.id )) AS student_fl FROM `Schedule` LEFT JOIN `Subject` ON `Schedule`.subject = `Subject`.id WHERE `Schedule`.teacher = ? AND `Schedule`.date = ?',
                        [teacher_id, date_select],
                        (error, results) => {
                            if (error) reject(error);
                            else resolve({ results, dayIndex: j });
                        }
                    );
                });
            });

            const scheduleResults = await Promise.all(schedulePromises);
            scheduleResults.forEach(({ results, dayIndex }) => {
                if (results.length) {
                    results.forEach(item => {
                        mas_schedule[dayIndex][item.number_pair - 1] = {
                            number_pair: item.number_pair,
                            name: item.name || '',
                            room: item.room || '',
                            stud_list : item.student_fl || '',
                            group: item.group_name
                        };
                    });
                }
            });
        }

        return res.render('schedule', { 
            pair: pair, 
            schedule: mas_schedule, 
            dates: formattedWeekDates
        });

    } catch (error) {
        console.error('Error fetching schedule:', error);
        return res.status(500).send('Error fetching schedule');
    }
};

exports.select_schedule = async (req, res) => {
    const { date_select } = req.body;
    if (date_select==null || date_select==NaN || date_select=='' || date_select==' ') {
        res.render('change_a',{ error : "Вы не указали дату"})
    } else {
        const [last_name, first_name, middle_name] = req.session.name.split(" ");
        try {
            const teacherResults = await new Promise((resolve, reject) => {
                con.query('SELECT id FROM `Teacher` WHERE login = ? AND first_name = ? AND last_name = ? LIMIT 1',
                    [req.session.login, first_name, last_name],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            });

            if (!teacherResults || !teacherResults.length) {
                return res.redirect('/');
            }

            const teacher_id = teacherResults[0].id;

            const date_select_schedule = await new Promise((resolve, reject) => {
                con.query('SELECT `Schedule`.number_pair, `Subject`.name, `Schedule`.room, `Group`.name as group_name FROM `Schedule` LEFT JOIN `Subject` ON `Schedule`.subject = `Subject`.id LEFT JOIN `Group` ON `Schedule`.group = `Group`.id WHERE `Schedule`.teacher = ? AND `Schedule`.date = ?',
                    [teacher_id, date_select],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            });

            const count_pair = await new Promise((resolve, reject) => {
                con.query('SELECT COUNT(`Timepair`.id) as pairs FROM `Timepair`',
                    (error,results) => {
                        if (error) reject(error);
                        else resolve(results[0]);
                    }
                ); 
            });

            let arr = new Array(count_pair.pairs).fill(0);
            let promises = [];
            
            arr.forEach((_, index) => {
                const promise = new Promise((resolve, reject) => {
                    con.query('SELECT `Schedule`.room as rooms FROM `Schedule` WHERE `Schedule`.date = ? AND `Schedule`.number_pair = ?',
                        [date_select, index + 1],
                        (error, results) => {
                            if (error) reject(error);
                            else resolve(results);
                        }
                    );
                });
            
                promises.push(promise);
            });
            
            const occupiedPremisesResults = await Promise.all(promises);
            arr = occupiedPremisesResults.map(result => result.map(r => r.rooms));
            
            let vacant_premises = await new Promise((resolve, reject) => {
                con.query('SELECT `Audience`.room_name FROM `Audience`',
                    (error,results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                )
            });

            vacant_premises.forEach((_,index) => {
                vacant_premises[index]=vacant_premises[index].room_name;
            })

            let result = [];
                
            for(let i = 0; i < count_pair.pairs; i++) {
                let occupiedRooms = arr[i] || [];
                
                let freeRooms = vacant_premises.filter(room => {
                    return !occupiedRooms.includes(room);
                });
                
                result.push(freeRooms);
            }
                        
            return res.render('change_a',{selectedDate : date_select, options_list: date_select_schedule, room_options_list : result});

        } catch (error) {
            console.error('Error fetching date:', error);
            return res.status(500).send('Error fetching date');
        }
    }
};

exports.change_schedule_room = async (req,res) => {
    const { date_select, pair_number, pair_name, new_room } = req.body;
    try {
        const teacherResults = await new Promise((resolve, reject) => {
            const [last_name, first_name, middle_name] = req.session.name.split(" ");
            con.query('SELECT id FROM `Teacher` WHERE login = ? AND first_name = ? AND last_name = ? LIMIT 1',
                [req.session.login, first_name, last_name],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        });

        if (!teacherResults || !teacherResults.length) {
            return res.redirect('/');
        }

        const teacher_id = teacherResults[0].id;

        const old_info = await new Promise((resolve, reject) => {
            con.query('SELECT `Schedule`.room FROM `Schedule` WHERE `Schedule`.teacher = ? AND `Schedule`.number_pair = ? AND `Schedule`.date = ? AND `Schedule`.subject = (SELECT `Subject`.id FROM `Subject` WHERE `Subject`.name = ? LIMIT 1) LIMIT 1',
                [teacher_id,pair_number,date_select,pair_name],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        })

        const update_schedule_room = await new Promise((resolve, reject) => {
            con.query('UPDATE `Schedule` SET `Schedule`.room = REPLACE(room, ? , ? ) WHERE `Schedule`.teacher = ? AND `Schedule`.number_pair = ? AND `Schedule`.date = ? ',
                [old_info[0].room,new_room,teacher_id,pair_number,date_select],
                (error,results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
    });
    
    let message = "Занятие по "+String(pair_name)+" "+String(pair_number)+" парой "+String(date_select)+" изменена на аудиторию "+String(new_room);
    return res.render('change_a',{ error : message})

    } catch (error) {
        console.error('Error:', error);
        return res.status(500).send('Error fetching date');
    }
}

exports.get_group_list = async (req, res) => {
    try{
        const group_list_name = await new Promise((resolve, reject) => {
            con.query('SELECT `Group`.name FROM `Group`',
                (error,results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            )
        });
        return res.render('mark_s',{ group_list : group_list_name })
    } catch(error){
        console.error('Error:', error);
        return res.status(500).send('Error fetching groups');
    }
};

exports.get_schedule_and_student = async (req, res) => {
    const { date_select, group_name_list } = req.body;
    if (date_select==null || date_select==NaN || date_select=='' || date_select==' ') {
        const group_list_name = await new Promise((resolve, reject) => {
            con.query('SELECT `Group`.name FROM `Group`',
                (error,results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            )
        });
        return res.render('mark_s',{ error : "Вы не указали дату", date: date_select, group_list : group_list_name})
    } else {
        const [last_name, first_name, middle_name] = req.session.name.split(" ");
        try {
            const teacherResults = await new Promise((resolve, reject) => {
                con.query('SELECT id FROM `Teacher` WHERE login = ? AND first_name = ? AND last_name = ? LIMIT 1',
                    [req.session.login, first_name, last_name],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            });

            if (!teacherResults || !teacherResults.length) {
                return res.redirect('/');
            }

            const teacher_id = teacherResults[0].id;

            const date_select_schedule = await new Promise((resolve, reject) => {
                con.query('SELECT `Schedule`.number_pair, `Subject`.name, `Schedule`.room FROM `Schedule` LEFT JOIN `Subject` ON `Schedule`.subject = `Subject`.id WHERE `Schedule`.teacher = ? AND `Schedule`.date = ? AND `Schedule`.group = (SELECT `Group`.id FROM `Group` WHERE `Group`.name = ? LIMIT 1)',
                    [teacher_id, date_select, String(group_name_list)],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            });

            const group_list_name = await new Promise((resolve, reject) => {
                con.query('SELECT `Group`.name FROM `Group`',
                    (error,results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                )
            });

            const list_all_stud_in_group = await new Promise((resolve, reject) => {
                con.query('SELECT CONCAT(`Student`.first_name, " ", `Student`.last_name) AS student FROM `Students_in_group` JOIN `Student` ON `Student`.id = `Students_in_group`.student_code WHERE `Students_in_group`.group_code = (SELECT `Group`.id FROM `Group` WHERE `Group`.name = ? LIMIT 1) ',
                    [group_name_list],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                );
            })

            return res.render('mark_s',{date: date_select, subject: date_select_schedule, group_list : group_list_name, stud_group : list_all_stud_in_group, group_name_list : group_name_list});
        } catch(error){
            console.error('Error:', error);
            return res.status(500).send('Error fetching date');
        }
    }
};

exports.mark_a_student = async (req, res) => {
    const {date_select,group_select, pair_name, student_name, number_pair} = req.body;
    let stud = student_name.split(' ');
    try{
        const [last_name, first_name, middle_name] = req.session.name.split(" ");
        const teacherResults = await new Promise((resolve, reject) => {
            con.query('SELECT id FROM `Teacher` WHERE login = ? AND first_name = ? AND last_name = ? LIMIT 1',
                [req.session.login, first_name, last_name],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        });

        if (!teacherResults || !teacherResults.length) {
            return res.redirect('/');
        }

        const teacher_id = teacherResults[0].id;

        const schedule_id = await new Promise((resolve, reject) => {
            con.query('SELECT id FROM `Schedule` WHERE `Schedule`.date = ? AND `Schedule`.teacher = ? AND `Schedule`.group = (SELECT `Group`.id FROM `Group` WHERE `Group`.name = ? LIMIT 1) AND `Schedule`.subject = (SELECT `Subject`.id FROM `Subject` WHERE `Subject`.name = ? LIMIT 1) AND `Schedule`.number_pair = ? LIMIT 1',
                [date_select,teacher_id,group_select,String(pair_name),parseInt(number_pair)],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            )
        });

        const student_id = await new Promise((resolve, reject) => {
            con.query('SELECT id FROM `Student` WHERE `Student`.first_name = ? AND `Student`.last_name = ? LIMIT 1',
                [stud[0],stud[1]],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            )
        });

        const check_attendance = await new Promise((resolve, reject) => {
            con.query('SELECT id FROM `Attendance` WHERE `Attendance`.schedule_id = ? AND `Attendance`.student_id = ? LIMIT 1',
                [schedule_id[0].id,student_id[0].id],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            )
        });

        const group_list_name = await new Promise((resolve, reject) => {
            con.query('SELECT `Group`.name FROM `Group`',
                (error,results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            )
        });

        if (check_attendance.length > 0) {
            return res.render('mark_s',{ date: date_select, group_list : group_list_name, error: ("Студент "+String(student_name)+" уже был отмечен на занятии")})
        } else {
            const fin = await new Promise((resolve, reject) => {
                con.query('INSERT INTO `Attendance` (student_id, schedule_id) VALUES (?, ?)',
                    [student_id[0].id, schedule_id[0].id],
                    (error, results) => {
                        if (error) reject(error);
                        else resolve(results);
                    }
                )
            });

            return res.render('mark_s',{ date: date_select, group_list : group_list_name, error : ("Студент "+String(student_name)+" из группы "+String(group_select)+" отмечен на занятии по "+String(pair_name)+" - "+String(date_select))});
        }

    } catch(error) {
        console.error('Error:', error);
        return res.status(500).send('Error fetching date');
    }
};

exports.reset = async (req,res) => {
    try{
        console.log(req.session);
        test_code="";
        let chars = 'acdefhiklmnoqrstuvwxyz0123456789'.split('');
        for(let i=0; i<5; i++){
            let x = Math.floor(Math.random() * chars.length);
            test_code += chars[x];
        }

        const teacherResults = await new Promise((resolve, reject) => {
            con.query(
                'SELECT email FROM `Teacher` WHERE login = ?',
                [req.session.login],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        });

        if (teacherResults.length > 0) {
            sendMail(test_code, teacherResults[0].email);
            req.session.status = "teacher";
            reset_title = teacherResults[0].email;
            return res.render('reset_password',{title: teacherResults[0].email});
        }

        const studentResults = await new Promise((resolve, reject) => {
            con.query(
                'SELECT email FROM `Student` WHERE login = ?',
                [req.session.login],
                (error, results) => {
                    if (error) reject(error);
                    else resolve(results);
                }
            );
        });

        if (studentResults.length > 0) {
            sendMail(test_code, studentResults[0].email);
            req.session.status = "student";
            reset_title = studentResults[0].email;
            return res.render('reset_password',{title: studentResults[0].email});
        }

    }  catch (error) {
        console.error('Login error:', error);
        return res.render('authorization', {
            message: 'Server error occurred'
        });
    }
}

exports.edit = async (req,res) => {
    console.log(test_code);
    const { one, two, tree, four, five, pass, r_pass } = req.body;
    if(one === null || one === '')
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'The absence of the first character'
        });
    }
    if(two === null || two === '')
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'The absence of the second character'
        });
    }
    if(tree === null || tree === '')
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'the absence of the third character'
        });
    }
    if(tree === null || tree === '')
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'the absence of the third character'
        });
    }
    if(four === null || four === '')
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'the absence of the fourth character'
        });
    }
    if(five === null || five === '')
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'the absence of the fifth character'
        });
    }
    let code_secure = one+two+tree+four+five;
    if (!(code_secure === test_code))
    {
        return res.render('reset_password',{
            title: reset_title,
            message: 'The security password does not match'
        });
    } else {
        if (!(String(pass)===String(r_pass)) || (pass === null || pass ==='' || r_pass === null || r_pass ===''))
        {
            return res.render('reset_password',{
                title: reset_title,
                message: 'Passwords do not match each other'
            });
        }
        else {
            let hashedPassword_new = await bcrypt.hash(r_pass,8);
            if (req.session.status == "teacher"){
                con.query('UPDATE `Teacher` SET password = ? WHERE email = ? LIMIT 1', [hashedPassword_new, reset_title] , async (error,results) =>{
                    if (error)
                    {
                        return console.log(error);
                    }
                    else {
                        req.session.destroy();
                        return res.render('reset_password',{
                            title: reset_title,
                            message: 'Passwords update'
                        });
                    }
                });
            } else if ( req.session.status = "student"){
                con.query('UPDATE `Student` SET password = ? WHERE email = ? LIMIT 1', [hashedPassword_new, reset_title] , async (error,results) =>{
                    if (error)
                    {
                        return console.log(error);
                    }
                    else {
                        req.session.destroy();
                        return res.render('reset_password',{
                            title: reset_title,
                            message: 'Passwords update'
                        });
                    }
                });
            }
        }
    }
}

hbs.registerHelper('json', function(context) {
    return JSON.stringify(context);
});

