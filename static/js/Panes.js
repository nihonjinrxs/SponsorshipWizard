
// Explore Options here: http://layout.jquery-dev.com/documentation.cfm#Options
function Panes() {

    var width = $(window).width();
    var height = $(window).height();

    $('body').layout({
        applyDemoStyles: true,
        initClosed: true,
        fxName: "slide",
        fxSpeed: "slow",
        //spacing_closed: 14,
        //center: {
        //    initClosed: false,
        //    fxName: "slide",
        //    fxSpeed: "slow",
        //    spacing_closed: 14
        //},
        center__initClosed: false,
        south__initClosed: false,
        west__initClosed: false,
        east__initClosed: false,
        north__initClosed: false
    });
    var myLayout = $('body').layout();
    //myLayout.sizePane("north", Math.max(130,height/10));
    myLayout.sizePane("center", width/2);
    myLayout.sizePane("east", width/2);
    myLayout.sizePane("south", width/15);
}