const googlehome = require('google-home-notifier');
const language = 'ja';
const googlehome_ip_address = process.env.GOOGLE_HOME_IP;

exports.speak = (message) => {
    googlehome.device('リビング',language);
    googlehome.ip('192.168.8.51',language);
    //googlehome.accent('ja');
    googlehome.notify(message, function (res) {
        console.log(res);
    });
};
