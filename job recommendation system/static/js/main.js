$(function() {
        var i= 1;
        $('#addsummury').live('click', function() {
                $('<p><textarea class="form-control"  name="summury['+i+']" placeholder="Enter Skill Summury"></textarea><a href="#" id="removesummury">Remove</a></p>').appendTo('#skill_summury');
                i++;
                return false;
        });
        
        $('#removesummury').live('click', function() { 
                if( i > 0 ) {
                        $(this).parents('p').remove();
                        i--;
                }
                return false;
        });
});

$(function() {
        var i= 1;
        $('#addacademics').live('click', function() { 
                $('<div><p>Course<input type="text" class="form-control"  name="course['+i+']" placeholder="Enter Course"></p>'+
                '<p>University<input type="text" class="form-control"  name="university['+i+']" placeholder="Enter University"></p>'+
                '<p>Result<input type="number" class="form-control"  name="result['+i+']"  placeholder="Enter Result"></p>'+
                '<p>Passout Year<input type="number" class="form-control"  name="passout['+i+']" placeholder="Enter Passout Year"><a href="#" id="removeacademics">Remove</a></p></div>').appendTo('#academics');
                i++;
                return false;
        });
        
        $('#removeacademics').live('click', function() { 
                if( i > 0 ) {
                        $(this).parent().parent('div').remove();
                        i--;
                }
                return false;
        });
});

$(function() {
        var i= 1;
        $('#addactivities').live('click', function() { 
                $('<p><textarea class="form-control"  name="activities['+i+']" placeholder="Enter Activity"></textarea><a href="#" id="removeactivities">Remove</a></p>').appendTo('#curricular_activities');
                i++;
                return false;
        });
        
        $('#removeactivities').live('click', function() { 
                if( i > 0 ) {
                        $(this).parents('p').remove();
                        i--;
                }
                return false;
        });
});

$(function() {
        var i= 1;
        $('#addstrength').live('click', function() { 
                $('<p><textarea class="form-control"  name="strength['+i+']" placeholder="Enter Strength"></textarea><a href="#" id="removestrength">Remove</a></p>').appendTo('#strength');
                i++;
                return false;
        });

        $('#removestrength').live('click', function() { 
                if( i > 0 ) {
                        $(this).parents('p').remove();
                        i--;
                }
                return false;
               
        });        
});

let navItems= ['#form1', '#form2', '#form3', '#form4', '#form5', '#form6', '#form7', '#form8', '#form9'];
function handleNavigation(e) {
    var id =(e.target.getAttribute('data-value'))
    var id1 = navItems[navItems.indexOf(id) - 1]
    var a = 0

    $(id1).find(':input').each(function(e){	
        if(this.tagName != 'BUTTON'){
                if (!this.value){
                        this.focus()
                        a = 1
                }
                if(this.id == 'phone_check'){
                        var nm = this.value
                        if(nm.length != 10){
                        alert('enter 10 digit phone number')
                        }
                }

        }
    });

    if(a==0){
    navItems.map(function(item) {
        if(id === item ) {
            $(item).addClass("active");
        }
        else {
        $(item).removeClass("active");
        }
    
    })
}
}

let Items= ['#ug', '#puc', '#sslc'];
function handleNav(e) {
    var Id =(e.target.getAttribute('data-value'))
    Items.map(function(item) {
        if(Id === item ) {
            $(item).addClass("active");
        }
        else {
        $(item).removeClass("active");
        }
    })
}