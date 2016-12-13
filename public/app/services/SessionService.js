(function(module){
    'use strict';

    function SessionService(Request, $rootScope, $state, $q, $ionicLoading) {
        function login(email, password) {
            var deferred = $q.defer();
            $ionicLoading.show({
                template: '<ion-spinner icon="android"></ion-spinner>'
            });
            Request.post('/auth/', {email: email, password: password}).then(
                function(response){ // success
                    var data = response.data;
                    $rootScope.user = data;
                    // notify application user logged in
                    $rootScope.$broadcast("session:loggedIn", data);
                    // send to cashier shift state
                    if($rootScope.user.locations.length > 1) {
                        $ionicLoading.hide();
                        deferred.resolve(data);
                        $state.go('location');
                    } else if($rootScope.user.locations.length == 0) {
                        $ionicLoading.hide();
                        deferred.reject("User has no site associated!");
                    } else {
                        $ionicLoading.hide();
                        setLocation(data.locations[0]);
                        deferred.resolve(data);
                        $state.go('app.shift');
                    }
                },
                function(err){ // failure
                    deferred.reject(err.data.error);
                    $ionicLoading.hide();
                });
            return deferred.promise;
        }

        function setLocation(location) {
            $rootScope.location = location;
        }

        function getLocation() {
            return $rootScope.location;
        }

        function logout() {
            var deferred = $q.defer();
            var token = null || $rootScope.user.token;
            if(token) {
                $ionicLoading.show({
                    template: '<ion-spinner icon="android"></ion-spinner>'
                });
                Request.del('/auth/'+$rootScope.user.token).then(function(){
                    $rootScope.user = null;
                    $rootScope.$broadcast("session:loggedOut");
                    $state.go('login');
                    deferred.resolve();
                    $ionicLoading.hide();
                }, function(failure){
                    deferred.reject(failure.data.error);
                    $ionicLoading.hide();
                });
            } else {
                deferred.reject("Not logged in!");
                $rootScope.$broadcast("session:loggedOut");
                $state.go('login');
            }
            return deferred.promise;
        }

        function assureLogged() {
            if(!this.isLogged()) {
                $state.go('login');
            }
        }

        function isLogged() {
            return !!$rootScope.user;
        }

        function currentUser() {
            return $rootScope.user;
        }

        return {
            login: login,
            logout: logout,
            isLogged: isLogged,
            assureLogged: assureLogged,
            currentUser: currentUser,
            setLocation: setLocation,
            getLocation: getLocation
        }
    }

    module.factory('SessionService', ['Request', '$rootScope', '$state', '$q', '$ionicLoading', SessionService]);

})(angular.module('pulltabs.pos'));
