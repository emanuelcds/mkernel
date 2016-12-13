(function(module){
    'use strict';

    function Request($rootScope, $http, $ionicLoading) {
        var baseURL = 'http://localhost:5000/api/pos';

        function __getToken() {
            var token = "";
            if ($rootScope.user) {
                token = $rootScope.user.token || "";
            }
            return token
        }

        function get(uri) {
            return $http.get(baseURL+uri+"?token="+__getToken(), {accepts: 'application/json'});
        }

        function post(uri, data) {
            return $http.post(baseURL+uri+"?token="+__getToken(), data, {contentType: 'application/json'});
        }

        function del(uri) {
            return $http.delete(baseURL+uri+"?token="+__getToken());
        }

        function put(uri) {
            return $http.put(baseURL+uri+"?token="+__getToken(), data, {contentType: 'application/json'});
        }

        return {
            get: get,
            post: post,
            del: del,
            put: put
        }
    }

    module.service('Request', ['$rootScope', '$http', '$ionicLoading',  Request]);
})(angular.module('pulltabs.pos'));
