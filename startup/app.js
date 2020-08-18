(function () {

    'use strict';
    angular
        .module('app', ['ngRoute', 'ngCookies', 'ui.bootstrap', 'googlechart', 'hljs', 'dndLists'])
        .config(config)
        //.filter('ashtml', function ($sce) { return $sce.trustAsHtml; })
        .filter('ashtml', ['$sce',function ($sce) { return function(input) { return input&&input.indexOf('<p')>-1 ? $sce.trustAsHtml(input) : input; } }])
        .directive('enterpress', function () {
            return function (scope, element, attrs) {
                element.bind("keydown keypress", function (event) {
                    if(event.which === 13) {
                        scope.$apply(function (){
                            scope.$eval(attrs.enterpress);
                        });

                        event.preventDefault();
                    }
                });
            };
        })
        .directive('keypress', function () {
            return function (scope, element, attrs) {
                element.bind("keydown keypress", function (event) {
                    //if(event.which === parseInt(attrs.presskey)) {
                        if(attrs.keypressenabled) {
                        scope.$apply(function (){
                            scope.$eval(attrs.keypress);
                        });

                        if(attrs.preventdefault) event.preventDefault();
                    }
                });
            };
        }).filter('percentage', ['$filter', function ($filter) {
            return function (input, decimals) {
                return $filter('number')(input * 100, decimals) + '%';
            };
        }]).filter('jsonStringify', [function () {
            return function (input) {
                return JSON.stringify(input);
            };
        }])
        .run(run);
    
    config.$inject = ['$routeProvider', '$locationProvider', 'hljsServiceProvider'];
    function config($routeProvider, $locationProvider, hljsServiceProvider) {
        hljsServiceProvider.setOptions({
            // replace tab with 4 spaces
            tabReplace: '    ',
            languages: ['cs']
        });

        $routeProvider
            .when('/', {
                cache: false,
                controller: 'HomeController',
                templateUrl: function () { return '/template?p=home/home.view.html&t=' + $.now(); },
                controllerAs: 'vm'
            })

            .when('/home', {
                cache: false,
                controller: 'HomeController',
                templateUrl: function () { return '/template?p=home/home.view.html&t=' + $.now(); },
                controllerAs: 'vm'
            })

        //.otherwise({ redirectTo: '/' });
    }

    run.$inject = ['$rootScope', '$location', '$cookies', '$http', '$interval', '$timeout', '$window'];
    function run($rootScope, $location, $cookies, $http, $interval, $timeout, $window) {
        $rootScope.intervals = [];
        $rootScope.weather = {};

        var opts = {
            lines: 12 // The number of lines to draw
            , length: 30 // The length of each line
            , width: 6 // The line thickness
            , radius: 56 // The radius of the inner circle
            , scale: 1 // Scales overall size of the spinner
            , corners: 1 // Corner roundness (0..1)
            , color: '#eee' // #rgb or #rrggbb or array of colors
            , opacity: 0.1 // Opacity of the lines
            , rotate: 300 // The rotation offset
            , direction: 1 // 1: clockwise, -1: counterclockwise
            , speed: 1 // Rounds per second
            , trail: 21 // Afterglow percentage
            , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
            , zIndex: 2e9 // The z-index (defaults to 2000000000)
            , className: 'spinner' // The CSS class to assign to the spinner
            , top: '50%' // Top position relative to parent
            , left: '50%' // Left position relative to parent
            , shadow: false // Whether to render a shadow
            , hwaccel: false // Whether to use hardware acceleration
            , position: 'absolute' // Element positioning
        }

        var target = document.getElementById('spinner');
        $rootScope.spinner = new Spinner(opts).spin(target);

        function heartbeat() {
            $timeout(function () {
                heartbeat();
            }, 1000);
        }
        heartbeat();

        $rootScope.spin = false;
        // keep user logged in after page refresh
        $rootScope.globals = $cookies.getObject('globals') || {};
        if ($rootScope.globals.currentUser) {
            //console.log(JSON.stringify($rootScope.globals.currentUser));
            $rootScope.isUserLoggedIn = true;
            $rootScope.config = $rootScope.globals.currentUser.config;
            //$location.path('/');
        }

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            $rootScope.killIntervals();
            // if ($location.protocol() !== 'https') {
            //     $window.location.href = $location.absUrl().replace('http', 'https').replace('//www.', '//');
            // }
            // redirect to home page if not logged in and trying to access a restricted page
            //var restrictedPage = $.inArray($location.path(), ['/login', '/register', '/contact', '/home', '/portfolio', '/crypto', '/questionaire', '/']) === -1;
            var restrictedPage = $.inArray($location.path(), ['/admin', '/numbers']) >= 0;
            if (restrictedPage && !$rootScope.isUserLoggedIn) {
                $location.path('/');
            }
        });

        $rootScope.code = [];
        $rootScope.killIntervals = function () {
            // Let's kill some intervals...
            angular.forEach($rootScope.intervals, function (interval) {
                $interval.cancel(interval);
            });
            $rootScope.intervals.length = 0;
        }
    }

})();