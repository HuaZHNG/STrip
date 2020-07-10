<template>
    <transition name="el-fade-in">
        <el-card class="histogram-card" v-show="flag">
            <el-button @click="flag=false" style="float: right; padding: 3px 0; z-index: 1300; color: #fff" type="text" icon="el-icon-close" size="default"></el-button>
            <div style="position: relative; left:10%; margin-top: 20px;">
                <column-chart :data="testData" :stacked="true" width="800px" height="250px" :colors="['#fff']"></column-chart>
            </div>
        </el-card>
    </transition>
</template>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                testData: [
                    ['0', 1],
                    ['1', 2],
                    ['3', 10],
                    ['4', 15],
                    ['5', 36],
                    ['6', 56],
                    ['7', 67],
                    ['8', 138],
                    ['9', 221],
                    ['10', 123],
                    ['11', 234],
                    ['12', 211],
                    ['13', 178],
                    ['14', 108],
                    ['15', 226],
                    ['16', 322],
                    ['17', 253],
                    ['18', 198],
                    ['19', 178],
                    ['20', 207],
                    ['21', 137],
                    ['22', 103],
                    ['23', 78]
                ],
                flag: false,
                data: [],
            }
        },
        components: {},
        methods: {
            initData: function(latlng, timeStamp) {
                //v-loading指令
                //ajax请求拿数据
                // $.post(this.urlHeader + '/destinations/hotValue', {
                //         latitude: latlng.lat.toString(),
                //         longitude: latlng.lng.toString(),
                //         dayOfWeek: "1",
                //         time: "1514127149992",
                //         // time: timeStamp,
                //     },
                //     function(data) {
                //         console.log(data)
                //         //拿到数据
                //     })
                $.ajax({
                    crossDomain: true,
                    xhrFields: {
                        withCredentials: true
                    },
                    url: this.urlHeader + '/destinations/hotValue',
                    data: {
                        latitude: latlng.lat.toString(),
                        longitude: latlng.lng.toString(),
                        dayOfWeek: "1",
                        time: "1514127149992",
                        // time: timeStamp,
                    },
                    type: 'post',
                    success: function(data) {
                        console.log(data)
                        //拿到数据
                    }
                })
                //绘制直方图，设置flag为true
                this.flag = true
            },
        },
    }
</script>

<style>
    .histogram-card {
        position: relative;
        height: 20%;
        width: 79%;
        z-index: 12;
        background: rgba(0, 0, 0, 0.5);
        border-color: rgba(0, 0, 0, 0);
        left: 21%;
    }
</style>
