<template>
    <div>
        <nav class="navbar navbar-fixed-top my-navbar" role="navigation">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#example-navbar-collapse">
                          <span class="sr-only">Toggle navigation</span>
                          <span class="icon-bar"></span>
                          <span class="icon-bar"></span>
                          <span class="icon-bar"></span>
                        </button>
                    <div class="navbar-brand" width="100%" >{{title}}</div>
                </div>
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                    <ul class="nav navbar-nav navbar-right">
                        <ul class="nav navbar-nav">
                            <li><a href="#home" @click="toHome">Home<span class="sr-only">(current)</span></a></li>
                            <li class="dropdown shade">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Schemes <span class="caret"></span></a>
                                <ul class="dropdown-menu shade" role="menu">
                                    <li>
                                        <a href="#">Dangerous Heat Map</a>
                                    </li>
                                    <li>
                                        <a href="#">Infected Population Prediction</a>
                                    </li>
                                    <li>
                                        <a href="#">Route Planning</a>
                                    </li>
                                    <li>
                                        <a href="#">Hot Spot</a>
                                    </li>
                                    <li class="divider"></li>
                                    <li><a href="#">More...</a></li>
                                </ul>
                            </li>
                            <li data-toggle="modal" data-target="#about"><a href="#mine">About Me</a></li>
                            <li data-toggle="modal" data-target="#about"><a href="#">Help</a></li>
                            <li data-toggle="modal" data-target="#about"><a href="#">Logout</a></li>
                        </ul>
                    </ul>
                    <div class="tab-content">
                        <div class="tab-pane fade in active" id="mine">
                            <component :is="mine"></component>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>
    import demo from './demo';
    import mainPage from './mainPage';
    import planRoute from './planRoute'
    import mine from './mine'

    export default {
        name: 'navBar',
        props: ['currentView', 'title'],
        component: {
            demo,
            mine,
            mainPage,
        },
        data() {
            return {
                logo: 'static/images/logo.png',
                myView: this.currentView,
                mine: mine,
                mainPage: mainPage,
            }
        },
        methods: {
        },
        watch: {
            title(val) {
                $(".nav-brand").innerHTML = val;
            }
        },
    }
</script>

<style type="text/css">
    /* @import "../css/app_css.css"; */
    .navbar-brand {
        font-family: "Impact";
        color: #ffffff;
        font-size: 36px;
        margin-left: -130px !important;
    }
</style>