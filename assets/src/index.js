import $ from 'jquery'
import 'htmx.org'
import 'fomantic-ui/dist/semantic.css'

window.jQuery = $;
window.$ = $;
window.htmx = require('htmx.org');

$(".djangocms-event-modal-trigger").click(function () {
    $("#djangocms-event-detail").modal({
        onHidden: $("#djangocms-event-detail").html('')
    }).modal("show")
})
$('.ui.accordion').accordion()