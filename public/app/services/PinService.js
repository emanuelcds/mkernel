(function(){
    function PinService(Request, SessionService, $q, $rootScope, $ionicLoading) {
        return {
            getPin: function(number) {
                var deferred = $q.defer();
                Request.get('/pin/'+number).then(
                    function(data) {
                        deferred.resolve(data.data);
                    },
                    function(failure) {
                        deferred.reject(failure.data.error);
                    }
                );
                return deferred.promise;
            },
            getPins: function() {
                var deferred = $q.defer();
                Request.get('/pin/location/'+SessionService.getLocation().id).then(
                    function(data) {
                        deferred.resolve(data.data.objects)
                    },
                    function(failure) {
                        deferred.reject(failure.data.error);
                    }
                )
                return deferred.promise;
            },
            deletePin: function(number) {
                var deferred = $q.defer();
                $ionicLoading.show({
                    template: '<ion-spinner icon="android"></ion-spinner>'
                });
                Request.del('/pin/'+number).then(
                    function(data) {
                        $ionicLoading.hide();
                        deferred.resolve(data.data.message);
                    },
                    function(failure) {
                        $ionicLoading.hide();
                        deferred.reject(failure.data.error);
                    }
                );
                return deferred.promise;
            },
            createPin: function(value) {
                var deferred = $q.defer();
                var pinData = {
                    credits: value*100,
                    location: SessionService.getLocation().id
                };
                $ionicLoading.show({
                    template: '<ion-spinner icon="android"></ion-spinner>'
                });
                Request.post('/pin', pinData).then(
                    function(data) {
                        $ionicLoading.hide();
                        deferred.resolve(data.data);
                        $rootScope.$broadcast("pin:newPin");
                    },
                    function(failure) {
                        $ionicLoading.hide();
                        deferred.reject(failure.data.error);
                    }
                );
                return deferred.promise;
            },
            forceCashOut: function(number) {
                var deferred = $q.defer();
                $ionicLoading.show({
                    template: '<ion-spinner icon="android"></ion-spinner>'
                });
                Request.get('/pin/cashout/'+number).then(
                    function(result) {
                        $ionicLoading.hide();
                        $rootScope.$broadcast("pin:forcedCashout");
                        deferred.resolve(result.data);
                    },
                    function(failure) {
                        $ionicLoading.hide();
                        deferred.reject(failure.data.error);
                    }
                );
                return deferred.promise;
            },
            cashOutPin: function(number) {
                var deferred = $q.defer();
                $ionicLoading.show({
                    template: '<ion-spinner icon="android"></ion-spinner>'
                });
                Request.get('/pin/cashout/'+number).then(
                    function(result) {
                        $ionicLoading.hide();
                        deferred.resolve(result.data);
                    },
                    function(failure) {
                        $ionicLoading.hide();
                        deferred.reject(failure.data.error);
                    }
                );
                return deferred.promise;
            }
        }
    }

    angular.module('pulltabs.pos').factory('PinService', ['Request', 'SessionService', '$q', '$rootScope', '$ionicLoading', PinService]);
})();
