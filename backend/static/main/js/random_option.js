function chosenRandomOption (optionList, btn) {
    let dropdown = document.getElementById(optionList);
    var options = [];
    var chosenItems = [];
    function setOptions(){
       for(var i = 0; i < dropdown.options.length; i++)
            options.push(dropdown.options[i].value);
    }
    document.getElementById(btn).addEventListener("click", function(){
       options = options.filter( function( el ) {
            return chosenItems.indexOf( el ) < 0;
       });
       if(options.length == 0){
            setOptions();
            chosenItems = [];
       }
       var unSelectedRandom = options[Math.floor(Math.random() * options.length)]
       for(var i = 0; i < dropdown.options.length; i++){
            var current = dropdown.options[i]
            if ( current.value == unSelectedRandom ) {
                 dropdown.selectedIndex = i;
                 chosenItems.push(current.value);
                 current.click();
            }
       }
    });
}