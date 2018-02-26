const exec = require('child_process').exec;
const google = require('./speak');
const language = 'ja';

const fetchRubbishdayInfo = () => {
    return new Promise(function(resolve, reject) {
        let text = ''
        exec("python3 rubbish.py", function(error, stdout, stderr) {
            text = stdout.replace(/\r?\n$/,"");
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
    fetchRubbishdayInfo().then(function(text) {
        google.speak(text);
        res.status(200).send(text);
    }).catch(function(error) {
        let content = 'エラーです';
        google.speak(content);
        res.status(200).send(content);
    });
}

exports.get_handler = (req, res, next) => {
    fetchRubbishdayInfo().then(function(text) {
        res.status(200).send(text);
    }).catch(function(error) {
        let content = 'エラーです';
        res.status(200).send(content);
    });
}
