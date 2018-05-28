class Editor {
    constructor (idAddAdvantages) {
        this.idAddAdvantages = idAddAdvantages
        $('#'+idAddAdvantages).select2({
          minimumInputLength: 3,
          ajax: {
            url: 'http://localhost:8001/advantages/',
            processResults: function (data) {
              console.log(data)
              return {
                results: $.map(data, function (item) {
                        console.log(item)
                        return {
                            text: item.fields.name,
                            id: item.pk
                        }
                    })
              };
            }
          }
        });
    }
    handleAddAdvantages () {
        var self = this
        $('#'+self.idAddAdvantages).on("change", function(e) {
            var selected = $('#'+self.idAddAdvantages).select2().find(":selected")
            $.get( "http://localhost:8001/advantage/" + selected.val() + "/", function( data ) {
              console.log(data)
            });
        });
    }
}