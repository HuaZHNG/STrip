// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import 'element-ui/lib/theme-chalk/index.css'
// import ElementUI from 'element-ui'
import Option from 'element-ui/lib/option';
import DatePicker from 'element-ui/lib/date-picker';
import Input from 'element-ui/lib/input';
import Button from 'element-ui/lib/button';
import Card from 'element-ui/lib/card';
import Radio from 'element-ui/lib/radio';
import RadioGroup from 'element-ui/lib/radio-group';
import RadioButton from 'element-ui/lib/radio-button';
import Upload from 'element-ui/lib/upload';
import ToolTip from 'element-ui/lib/tooltip';
import Rate from 'element-ui/lib/rate';
import Switch from 'element-ui/lib/switch';
import Message from 'element-ui/lib/message';

import Chartkick from 'chartkick'
import VueChartkick from 'vue-chartkick'
import Chart from 'chart.js'

import VueAMap from 'vue-amap'

Vue.config.productionTip = false

Vue.use(DatePicker);
Vue.use(Input);
Vue.use(Button);
Vue.use(Card);
Vue.use(Upload);
Vue.use(Option)
Vue.use(Radio);
Vue.use(RadioGroup);
Vue.use(RadioButton);
Vue.use(ToolTip);
Vue.use(Switch);
Vue.use(Message)
Vue.use(VueChartkick, {
    Chartkick
});
// Vue.use(ElementUI);

Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    template: '<App/>',
    components: { App }
})

//全局变量header
Vue.prototype.urlHeader = 'http://10.60.43.111:18888'