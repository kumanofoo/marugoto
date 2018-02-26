const exec = require('child_process').exec;
const google = require('./speak');
const language = 'ja';


const fetchRealtimeBusInfo = () => {
    return new Promise(function(resolve, reject) {
        let text = ''
        exec("python bus.py", function(error, stdout, stderr) {
            next_bus = stdout.split("\n");
            next_bus.forEach(function(val, index, array) {
                if (val) {
                    let t = parseInt(val, 10);
                    if (t) {
                        let hour = String(Math.floor(t/100));
                        let minute = String(t % 100);
                        if (text) {
                            text += 'その次は、';
                        }
                        text += hour + '時' + minute + '分、';
                    }
                }
            });
            if (text) {
                resolve(text);
            }
            else {
                reject(text);
            }
        });
    });
}

exports.post_handler = (req, res, next) => {
    fetchRealtimeBusInfo().then(function(dia) {
        let content =  '次のバスは、' + dia + 'です';
        google.speak(content);
        res.status(200).send(content);
    }).catch(function(error) {
        let content = 'これからのバスはありません';
        google.speak(content);
        res.status(200).send(content);
    });
}

exports.get_handler = (req, res, next) => {
    fetchRealtimeBusInfo().then(function(dia) {
        let content =  '次のバスは、' + dia + 'です';
        res.status(200).send(content);
    }).catch(function(error) {
        let content = 'これからのバスはありません';
        res.status(200).send(content);
    });
}
