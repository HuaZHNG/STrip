<template>
    <div>
        <div>
            <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
                <!-- Indicators -->
                <ol class="carousel-indicators">
                    <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
                    <li data-target="#carousel-example-generic" data-slide-to="1"></li>
                    <li data-target="#carousel-example-generic" data-slide-to="2"></li>
                </ol>
                <div class="carousel-inner" role="listbox">
                    <div class="item active">
                        <a href="#">
                            <img :src="routePlanning" width="100%" @click="currentChange('dangerousHeatMap')">
                            <div class="carousel-caption" @click="currentChange('dangerousHeatMap')">
                                <!--<h1>Dangerous Heat Map</h1>-->
                                <h1>Risk <br> Mapping</h1>
                                <p></p>
                            </div>
                        </a>
                    </div>
                    <div class="item">
                        <a href="#">
                            <img :src="prediction" @click="currentChange('infectedPopulationPrediction')">
                            <div class="carousel-caption" @click="currentChange('infectedPopulationPrediction')">
                                <!--<h1>Infected Population Prediction</h1>-->
                              <h1>Close Contacts <br> Tracking</h1>
                              <p></p>
                            </div>
                        </a>
                    </div>
                    <div class="item">
                        <a href="#">
                            <img :src="img1" @click="currentChange('planRoute')">
                            <div class="carousel-caption" @click="currentChange('planRoute')">
                                <h1>Route <br> Planning</h1>
                                <p></p>
                            </div>
                        </a>
                    </div>
                </div>
                <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
                    <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                </a>
                <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
                    <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                </a>
            </div>
            <div class="row">
                <div class="middle-part grid col-md-4" @click="currentChange('dangerousHeatMap')" style="margin-right:100px;">
                    <figure class="effect-sadie">
                        <a><img class="ex_img" :src="thermogramImg" @click="currentChange('dangerousHeatMap')"></a>
                        <h2>Risk <span> Mapping</span></h2>
                    </figure>
                </div>
                <div class="middle-part grid col-md-4" @click="currentChange('hotSpot')" style="margin-right:100px;">
                    <figure class="effect-sadie">
                        <a><img class="ex_img" :src="hotSpotImg" @click="currentChange('hotSpot')"></a>
                        <h2>Close-Contacts <span>Tracking</span></h2>
                    </figure>
                </div>
                <div class="middle-part grid col-md-4" @click="currentChange('planRoute')" style="margin-right:100px;">
                    <figure class="effect-sadie">
                        <a><img class="ex_img" :src="planRouteImg" @click="currentChange('planRoute')"></a>
                        <h2>Route<span>Planning</span></h2>
                    </figure>
                </div>
            </div>
        </div>
        <footer>
            <div class="container setFooter">
                <p>Copyright © 2020-2021 HongNiangZi</p>
                <p>版权所有 © 2020-2021 红娘子军团</p>
            </div>
        </footer>
    </div>
</template>

<script>
    import demo from "./demo.vue";
    import thermogram from "./thermogram.vue";
    import planRoute from "./planRoute.vue";
    import hotSpot from './hotSpot.vue'
    export default {
        name: "mainPage",
        data() {
            return {
                img1: "static/images/map.jpg",
                logo: "static/images/logo.png",
                img2: "static/images/map_ex.png",
                prediction: "static/images/prediction.png",
                routePlanning: "static/images/routePlanning.png",
                thermogramImg: "static/images/thermogram.jpg",
                planRouteImg: "static/images/routePlan.jpg",
                hotSpotImg: 'static/images/hotspot_ex.png',
                demo: demo,
                planRoute: planRoute,
                thermogram: thermogram,
                hotSpot: hotSpot
            };
        },
        props: ["currentView"],
        methods: {
            currentChange: function(str) {
                switch (str) {
                    case "dangerousHeatMap":
                        // this.myView = demo
                        // this.$emit("change-title", "Dangerous-Heat-Map");
                        this.$emit("change-title", "Risk-Mapping");
                        this.$emit("main-on-change", demo);
                        break;
                    case "infectedPopulationPrediction":
                        // this.myView = thermogram
                        // this.$emit("change-title", "Infected-Population-Prediction");
                        this.$emit("change-title", "Close-Contact-Tracking");
                        this.$emit("main-on-change", thermogram);
                        break;
                    case "planRoute":
                        // this.myView = planRoute
                        this.$emit("change-title", "Route-Planning");
                        this.$emit("main-on-change", planRoute);
                        break;
                }
            }
        },
        watch: {}
    };
    $(window).scroll(function() {
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav");
        }
    });
</script>

<style scoped type="text/css">
    @import "../css/set1.css";
    @import "../css/app_css.css";
    .setFooter {
        background: #26292f;
        height: 90px;
        width: 100%;
        position: relative;
        top: 120px;
        z-index: 13;
    }
    .setFooter p {
        position: relative;
        left: 40px;
        top: 18px;
        color: white;
        font-weight: 200;
        font-family: Helvetica Neue;
        font-size: 13px;
    }
</style>
