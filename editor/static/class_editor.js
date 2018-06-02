function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({   headers: {  "X-CSRFToken": csrftoken  }  });

class Attribute {
    constructor (idAdvantage, name, bonus, max) {
        this.id = idAdvantage
        this.name = name
        this.bonuses = [bonus]
        this.maximums = [max]
        this.max = 0
        this.total = 0
    }
    add(bonus, max) {
        this.bonuses.push(bonus)
        this.maximums.push(max)
    }
    calculate() {
        for (var i = 0; i < this.bonuses.length; i++) {
            this.total += this.bonuses[i]
        }
        for (var i = 0; i < this.maximums.length; i++) {
            if (this.maximums[i] > this.max)
            this.max = this.maximums[i]
        }
        if (this.total > this.max) {
            this.total = this.max
        }
    }
    draw() {
        if ($('#attr'+this.id).length > 0) {
            $('#attr'+this.id).html('')
            $('#attr'+this.id).append(this.name + ' : ' + this.total + ' (' + this.max + ')')
        } else {
            $('#attributes-body').append('<div id="attr'+this.id+'"></div>')
            $('#attr'+this.id).append(this.name + ' : ' + this.total + ' (' + this.max + ')')
        }
        this.total = 0
        this.max = 0
    }
}

class Editor {
    createSelect2() {
        $('#'+this.idAddAdvantages).select2({
          minimumInputLength: 3,
          ajax: {
            url: this.address + '/advantages/',
            processResults: function (data) {
              return {
                results: $.map(data, function (item) {
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
    getAdvantageIds() {
        var self = this
        var out = []
        for (var i = 0; i < self.advantages.length; i++) {
            out.push(self.advantages[i].id)
        }
        return out
    }
    handleSave() {
        var self = this
        $('#save').on('click', function() {
            var character = {
                advantages: self.getAdvantageIds(),
                first_name: $('#first_name').val(),
                last_name: $('#last_name').val(),
                nickname: $('#nickname').val(),
                total_pc: $('#total_pc').val()
            }
            $.post(self.address + '/save_character/', character)
            .done(function( data ) {
                console.log('save !', data)
            });
        })
    }
    fetchExistingAdvantages() {
        var self = this
        $('.advantage').each(function() {
            var advantageName = $(this).children('.advantage-name').text().trim()
            var advantageId = $(this).children('.advantage-name').data('id')
            var bonuses = []
            $(this).find('.attribute').each(function() {
                bonuses.push({
                    'attribute_name': $(this).children('.attribute-name').text().trim(),
                    'attribute': $(this).children('.attribute-name').data('id'),
                    'bonus': $(this).children('.attribute-value').text(),
                    'max': $(this).children('.attribute-max').text()
                })
            })
            var adv = {'id': advantageId, 'name': advantageName, 'bonuses': bonuses}
            self.advantages.push(adv)
        })
        for (var i = 0; i < self.advantages.length; i++) {
            self.pushAttributesFromAdvantage(i, self.advantages[i])
        }
    }
    constructor (idAddAdvantages, address) {
        this.idAddAdvantages = idAddAdvantages
        this.address = address
        this.advantages = []
        this.attributes = {}
        this.createSelect2()
        this.handleSave()
        this.fetchExistingAdvantages()
    }
    pushAttributesFromAdvantage(index, advantage) {
        var self = this

        for (var j = 0; j < advantage.bonuses.length; j++) {
            if (!(advantage.bonuses[j].attribute in self.attributes)) {
                self.attributes[self.advantages[index].bonuses[j].attribute] = new Attribute(
                    self.advantages[index].bonuses[j].attribute,
                    self.advantages[index].bonuses[j].attribute_name,
                    parseInt(self.advantages[index].bonuses[j].bonus),
                    parseInt(self.advantages[index].bonuses[j].max),
                )
            } else {
                self.attributes[self.advantages[index].bonuses[j].attribute].add(
                    parseInt(self.advantages[index].bonuses[j].bonus),
                    parseInt(self.advantages[index].bonuses[j].max)
                )
            }
            self.attributes[self.advantages[index].bonuses[j].attribute].calculate()
            self.attributes[self.advantages[index].bonuses[j].attribute].draw()
            $('#a'+self.advantages[index].id+' .box-body').append(
                '<span>' + self.advantages[index].bonuses[j].attribute_name + ': +' + self.advantages[index].bonuses[j].bonus +
                '(' + self.advantages[index].bonuses[j].max + ')'
                + '</span><br>')
        }
    }
    buildAdvantages() {
        var self = this
        $('#advantages').html('')
        for (var i = 0; i < self.advantages.length; i++) {
            $('#advantages').append('<div id="a'+self.advantages[i].id+'" class="box">')
            $('#a'+self.advantages[i].id).append('<div class="box-head">'+self.advantages[i].name + '</div>')
            $('#a'+self.advantages[i].id).append('<div class="box-body">')
            self.pushAttributesFromAdvantage(i, self.advantages[i])
            $('#a'+self.advantages[i].id).append('</div></div>')
        }
    }
    handleAddAdvantages () {
        var self = this
        $('#'+self.idAddAdvantages).on('select2:select', function(e) {
            var selected = $('#'+self.idAddAdvantages).select2().find(':selected')
            if (selected.val() && selected.val() != 'undefined') {
                $.get( self.address + '/advantage/' + selected.val() + '/', function( data ) {
                  self.advantages.push(data)
                  self.attributes = {}
                  self.buildAdvantages()
                  $('#'+self.idAddAdvantages).val(null).trigger('change.select2')
                  self.createSelect2()
                });
            }
        });
    }
}