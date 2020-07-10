<template>
  <transition name="el-fade-in">
    <div id="block" name="block">
      <div>
        <div id="search-box">
          <i class="icon-locate"></i>
          <input class="start" type="text" name="start" placeholder="Search Your Destinations" v-on:focus="focus()">
        </div>
      </div>
      <div id="timepicker">
        <el-date-picker v-model="departure" type="datetime" placeholder="Choose Or Generate" format="yyyy-MM-dd HH:mm" value-format="yyyy-MM-dd HH:mm" size="mini" style="width: 200px;" :picker-options="startPickerOptions" @change="onStartDatetimeChanged()"></el-date-picker>
        <el-radio-group v-model="transportation" style="position: relative; width: 200px; top: 8px; left: 0" size="mini" fill="#26282D" @change="transportationChange">
          <el-radio-button label="Drive" id="radioBut"></el-radio-button>
          <el-radio-button label="Walk" id="radioBut"></el-radio-button>
          <el-radio-button label="Metro/Bus" id="radioBut"></el-radio-button>
        </el-radio-group>
        <el-date-picker v-if="ifArriveTimeBoxShow" v-model="arrival" type="datetime" placeholder="Choose Arrival Time" format="yyyy-MM-dd HH:mm" value-format="yyyy-MM-dd HH:mm" size="mini" style="width: 200px; top: 10px;" :picker-options="endPickerOptions" @change="onEndDatetimeChanged()"
          v-show="ifArriveTimeBoxShow"></el-date-picker>
        <el-date-picker v-if="!ifArriveTimeBoxShow" disabled type="datetime" placeholder="Choose Arrival Time" style="width: 200px; top: 10px;" size="mini"></el-date-picker>
      </div>
    </div>
  </transition>
</template>

<script>
  import {
    TimeKnots
  } from '../assets/js/timeknots.js'
  import CircleMenu from 'vue-circle-menu'
  import Multiselect from 'vue-multiselect'
  import AMap from 'AMap'
  export default {
    data() {
      let x = this
      return {
        searchOption: {
          city: '上海',
          citylimit: true,
          autoFitView: true,
        },
        test: "",
        markers: [],
        departure: "",
        arrival: "",
        startPickerOptions: {
          disabledDate(time) {
            let now = Date.now() - 24 * 3600 * 1000
            let next = Date.now() + 6 * 24 * 3600 * 1000
            // let timeSpace = time.getTime() < now && time.getTime() > next
            let cur = time.getTime()
            let timeSpace = cur > next || cur < now
            // console.log(timeSpace)
            return timeSpace
          }
        },
        endPickerOptions: {
          disabledDate(time) {
            let next = Date.now() + 6 * 24 * 3600 * 1000
            let now = x.departure.length == 0 ? Date.now() - 24 * 3600 * 1000 : new Date(x.departure) - 24 * 3600 * 1000
            // let timeSpace = time.getTime() < now && time.getTime() > next
            let cur = time.getTime()
            let timeSpace = cur > next || cur < now
            // console.log(timeSpace)
            return timeSpace
          }
        },
        transportation: 'Drive',
        trash: "../../static/images/trash.png",
        ifListenStartInput: true,
        ifListenEndInput: true,
        map: null,
        identifier: 0,
        ifArriveTimeBoxShow: true,
      }
    },
    // props: ['map'],
    methods: {
      drawTimeLineRect: function() {
        var timeline = document.createElement('div')
        timeline.id = "timeline" + this.identifier
        //timeline样式
        timeline.style.position = "relative"
        timeline.style.top = "-30px"
        timeline.style.zIndex = 12
        timeline.style.left = "10px"
        var trash = document.createElement('div')
        trash.id = "trash"
        var trashImg = document.createElement('img')
        trashImg.src = this.trash
        trashImg.onclick = this.clear
        trash.appendChild(trashImg)
        let index = this.$parent.pickers.length - 1
        document.getElementsByName("block")[index].appendChild(timeline)
        document.getElementsByName("block")[index].appendChild(trash)
        var arr = [{
          "value": 224,
          "name": "Departure Time"
        }, {
          "value": 255,
          "name": "Arrival Time"
        }]
        let div = "#timeline" + this.identifier
        TimeKnots.draw(div, arr, {
          dateDimension: false,
          showLabels: false,
          radius: 4,
          horizontalLayout: false,
          width: 20,
          color: "#26282D",
          height: 80,
          lineWidth: 2,
        });
      },
      onStartDatetimeChanged: function() {
        if (this.departure >= this.arrival && this.arrival.length != 0) {
          alert("Departure time must be later than Arrival time!")
          this.departure = ""
          return
        } else if (this.departure.length == 0) {
          return
        }
        var timeStamp = (new Date(this.departure)).valueOf()/1000
        this.$parent.removePreArrTimeAddNew(this.identifier, timeStamp)
      },
      onEndDatetimeChanged: function() {
        // var startPicker = this.$refs.startpicker.control;
        // startPicker.maxDate(newEnd);
        if (this.departure >= this.arrival && this.departure.length != 0) {
          alert("Arrival time must be earlier than Departure time!")
          this.arrival = ""
          return
        } else if (this.arrival.length == 0) {
          return
        }
        var timeStamp = (new Date(this.arrival)).valueOf()/1000
        this.$parent.removePreArrTimeAddNew(this.identifier, timeStamp)
      },
      clear: function() {
        this.$parent.clearPickerBlock(this.identifier)
      },
      autoComplete: function(target) {
        let self = this
        AMap.plugin(['AMap.Autocomplete', 'AMap.PlaceSearch'], function() {
          var autoOptions = {
            city: "上海", //城市，默认全国
            input: target //使用联想输入的input的id
          };
          var autocomplete = new AMap.Autocomplete(autoOptions);
          AMap.event.addListener(autocomplete, "select", function(e) {
            //TODO 针对选中的poi实现自己的功能
            //marker
            if (target == "start" + self.identifier) {
              self.removePreAddNew(e.poi, "start")
            }
            // else {
            //   self.removePreAddNew(e.poi, "end")
            // }
            //通知直方图变化
            self.setHistogramData(e.poi.location)
          });
        });
      },
      focus: function() {
        //判断start和end是否执行autocomplete的函数
        if (this.ifListenStartInput) {
          this.autoComplete("start" + this.identifier)
          this.ifListenStartInput = false
        }
        // if (this.ifListenEndInput) {
        //   this.autoComplete("end" + this.identifier)
        //   this.ifListenEndInput = false
        // }
        //直方图消失
        this.$parent.setHistogramFlagFalse()
      },
      removePreAddNew: function(poi, startOrEnd) {
        let self = this
        //除掉旧的marker增加新的marker
        if (startOrEnd == "start") {
          this.$parent.removeMarker((self.identifier))
          this.$parent.addMarker(poi, self.identifier, this.transportation)
        }
        // else if (startOrEnd == "end") {
        //   this.$parent.removeMarker((self.identifier+1) * 2)
        //   this.$parent.addMarker(poi, (self.identifier+1) * 2)
        // } 
        else {
          return
        }
      },
      setHistogramData: function(latlng) {
        //通知直方图变化
        this.$parent.setHistogramData(latlng)
      },
      transportationChange: function() {
        this.$parent.changeTransportation(this.identifier, this.transportation)
      }
    },
    components: {
      'circle-menu': CircleMenu,
      'multiselect': Multiselect
    },
    mounted() {
      //初始化identifier
      this.identifier = this.$parent.getIdentifier()
      //保证组件在document中
      this.$nextTick(function() {
        //画时间轴
        this.drawTimeLineRect()
        //改变searchbox id
        var startBox = document.getElementsByName("start")[this.$parent.pickers.length - 1]
        startBox.id = "start" + this.identifier
        // var endBox = document.getElementsByName("end")[this.$parent.pickers.length-1]
        // endBox.id = "end" + this.identifier
        //改变placeHolder
        if (this.$parent.pickers.length == 1) {
          startBox.setAttribute('placeholder', 'Search Your Start Point')
          this.ifArriveTimeBoxShow = false
          this.$parent.removePreArrTimeAddNew(this.identifier, 1515392760)
        }
      })
    }
  }
</script>

<style>
  #block {
    position: relative;
    height: 190px;
    width: 265px;
    background: #ffffff;
    box-shadow: 0px, 2px, 10px, #26282D;
    left: 2.5%;
    border-radius: 3px;
    border: 0.1px solid #26282D;
    margin: 0 10px 10px 10px;
  }
  #search-box {
    position: relative;
    width: 220px;
    height: 30px;
    top: 20px;
    left: 25px;
    font-size: 4px;
    color: #26282D;
    font-weight: 250;
  }
  .start {
    position: relative;
    width: 220px;
    height: 32px;
    border: none;
    box-shadow: 2px 2px 5px #CBCBCB;
    padding-inline-start: 30px;
    padding-inline-end: 20px;
  }
  .end {
    position: relative;
    width: 220px;
    height: 32px;
    border: none;
    box-shadow: 2px 2px 5px #CBCBCB;
    padding-inline-start: 30px;
    padding-inline-end: 20px;
    top: 15px;
  }
  #destination {
    position: relative;
    top: 15px;
    /* left: 20px; */
  }
  input::-webkit-input-placeholder {
    color: #9B9B9B;
    font-size: 5px;
    font-weight: 200;
  }
  input::-moz-placeholder {
    color: #9B9B9B;
    font-size: 5px;
    font-weight: 200;
  }
  input::-ms-input-placeholder {
    color: #9B9B9B;
    font-size: 5px;
    font-weight: 200;
  }
  #timeline {
    position: relative;
    left: 5%;
    z-index: 12;
    top: -30px;
  }
  #timepicker {
    position: relative;
    /* top: 10px; */
    left: 35px;
    top: 45px;
    z-index: 13;
  }
  #trash {
    position: relative;
    left: 245px;
    top: -45px;
    z-index: 100000;
    cursor: pointer;
  }
  .icon-locate {
    position: absolute;
    left: 8px;
    z-index: 5;
    margin-top: 8px;
    background-image: url('../../static/images/定位.png');
    /*引入图片图片*/
    background-repeat: no-repeat;
    /*设置图片不重复*/
    background-position: 0px 0px;
    /*图片显示的位置*/
    width: 40px;
    /*设置图片显示的宽*/
    height: 35px;
    /*图片显示的高*/
  }
  input:focus {
    outline: none;
  }
  #radioBut {
    font-weight: 200;
    width: 55px;
  }
</style>
