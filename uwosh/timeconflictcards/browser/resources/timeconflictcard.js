jq(document).ready(function(){  
        var term = jq("select[name= psterm]").val();
        var subject = jq("select[name= subject1]").val();
        var cat1 = jq("input[name= catalognumber1]").val();
        var catnum = new Array(); //array that holds catalog numbers after process
        var term = jq("select[name= psterm]").val();
        var subjects2 = jq("select[name= subject2]").val();
        var cat2 = jq("input[id= catalognumber2]").val();
        var sec1 = jq("input[name= sectionnumber1]").val();
        var sec2 = jq("input[name= sectionnumber2]").val();
        var class1 = jq("input[id= classnumber1]").val();
        var instructor1 = jq("input[id= instructorID1]").val();
        var class2 = jq("input[id= classnumber2]").val();
        var instructor2 = jq("input[id= instructorID2]").val();
        var secnum = new Array(); //array that holds catalog numbers after process
        var cat2num = new Array();
        var sec2num = new Array();
        var studentname = jq("input[name= fullname]").val();
        var studentsemail = jq("input[name= studentemail]").val();

        function getCat1 () {
          var get_catalog_number = "https://ws.it.uwosh.edu/getCatalogNumbersByTermAndSubjectJSONPCX?strm="+term+"&subject="+subject+"&callback=?";
          catnum.push("<option value='" + cat1 +"'>" + cat1 + "</option>");
          $.getJSON(get_catalog_number, function(data){
           $.each(data, function(i,items){
              catnum.push("<option value='" + items + "'>" + items + "</option>"); 
           });
          tagstringA = "<select name='catalognumber1' id= 'catalognumber1'>" + catnum.join(" ") + "</select>";
          jq("input[name=catalognumber1]").replaceWith(tagstringA);
          getSec1();
          });
        };
        
        function getSec1(){
          var get_section_number1 = "https://ws.it.uwosh.edu/getSectionNumbersByTermAndSubjectAndCatalogNumberJSONPCX?strm="+term+"&subject="+subject+"&catalog_nbr="+cat1+"&callback=?";
          secnum.push("<option value='" + sec1 +"'>" + sec1 + "</option>");
          $.getJSON(get_section_number1, function(data1){
           $.each(data1, function(i,item){
              secnum.push("<option value='" + item + "'>" + item + "</option>"); 
           });
           tagstringB = "<select name='sectionnumber1' id= 'sectionnumber1'>" + secnum.join(" ") + "</select>";
           jq("input[name= sectionnumber1]").replaceWith(tagstringB);
           getClassInfo();
          });   
        };

        function getClassInfo(){
            tagstring1 = '<div name="classnumber1fullname" class="blurrable firstToFocus">' + class1 + '</div>';
            jq("input[id= classnumber1]").after(tagstring1);
            jq("input[id= classnumber1]").hide();
            tagstring3 = '<div name="instructorID1fullname" class="blurrable firstToFocus">' + instructor1 + '</div>';
            jq("input[id= instructorID1]").after(tagstring3);
            jq("input[id= instructorID1]").hide();
           getCat2();
        };

        function getCat2(){
          var get_catalog_number = "https://ws.it.uwosh.edu/getCatalogNumbersByTermAndSubjectJSONPCX?strm="+term+"&subject="+subjects2+"&callback=?";
          cat2num.push("<option value='" + cat2 +"'>" + cat2 + "</option>");
          $.getJSON(get_catalog_number, function(data2){
            $.each(data2, function(i,itemi){
               cat2num.push("<option value='" + itemi + "'>" + itemi + "</option>"); 
            });
           tagstringc = "<select name='catalognumber2' id='catalognumber2'>" + cat2num.join(" ") + "</select>";
           jq("input[name= catalognumber2]").replaceWith(tagstringc);
           getSec2();
          });         
        };

        function getSec2(){
          var get_section_number2 = "https://ws.it.uwosh.edu/getSectionNumbersByTermAndSubjectAndCatalogNumberJSONPCX?strm="+term+"&subject="+subjects2+"&catalog_nbr="+cat2+"&callback=?";
          sec2num.push("<option value='" + sec2 +"'>" + sec2 + "</option>");
          $.getJSON(get_section_number2, function(data3){
            $.each(data3, function(i,itemes){
               sec2num.push("<option value='" + itemes + "'>" + itemes + "</option>"); 
            });
           tagstringd = "<select name='sectionnumber2' id='sectionnumber2'>" + sec2num.join(" ") + "</select>";
           jq("input[name= sectionnumber2]").replaceWith(tagstringd);
           getClassInfo2();
        });           
        };

         function getClassInfo2(){
            tagstring14 = '<div name="classnumber2fullname" class="blurrable firstToFocus">' + class2 + '</div>';
            jq("input[id= classnumber2]").after(tagstring14);
            jq("input[id= classnumber2]").hide();
            tagstring13 = '<div name="instructorID1fullname" class="blurrable firstToFocus">' + instructor2 + '</div>';
            jq("input[id= instructorID2]").after(tagstring13);
            jq("input[id= instructorID2]").hide();
        };

        function setFields(){
          tag100 = '<div name="studentfullname" class="blurrable firstToFocus">' + studentname + '</div>';
          tag101 = '<div name="studentsfullemail" class="blurrable firstToFocus">' + studentsemail + '</div>';
          jq("input[name= fullname]").replaceWith(tag100);
          jq("input[name= studentemail]").replaceWith(tag101);
          jq("input[name= catalognumber1]").hide();
          jq("input[name= sectionnumber1]").hide();
          jq("input[name= classnumber1]").hide();
          jq("input[name= instructorID1]").hide();
          jq("input[name= catalognumber2]").hide();
          jq("input[name= sectionnumber2]").hide();
          jq("input[name= classnumber2]").hide();
          jq("input[name= instructorID2]").hide();
        }
      
      if(subject != "na"){
        getCat1();
        }
      else{
        setFields();
      }

    jq("select[name= subject1]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subject = jq("select[name= subject1]").val();
        var catnum = new Array(); //array that holds catalog numbers after process
        var dash = new String();
        dash = " Please choose ";
        catnum.push("<option value='" + dash +"'>" + dash + "</option>");
        //var catoptions = new String();
        var get_catalog_number = "https://ws.it.uwosh.edu/getCatalogNumbersByTermAndSubjectJSONPCX?strm="+term+"&subject="+subject+"&callback=?";
        $.getJSON(get_catalog_number, function(data){
           $.each(data, function(i,item){
              catnum.push("<option value='" + item + "'>" + item + "</option>"); 
           });
          tagstring = "<select name='catalognumber1' id= 'catalognumber1'>" + catnum.join(" ") + "</select>";
          jq("input[name=catalognumber1]").replaceWith(tagstring);
          jq("select[name=catalognumber1]").replaceWith(tagstring);
        });           
    });

    jq("select[name= catalognumber1]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subjects = jq("select[name= subject1]").val();
        var cat1 = jq("select[name= catalognumber1]").val();
        var dash = new String();
        dash = " Please choose ";
        var secnum = new Array(); //array that holds catalog numbers after process
        secnum.push("<option value=" + dash +"'>" + dash + "</option>");
        //var catoptions = new String();
        var get_section_number1 = "https://ws.it.uwosh.edu/getSectionNumbersByTermAndSubjectAndCatalogNumberJSONPCX?strm="+term+"&subject="+subjects+"&catalog_nbr="+cat1+"&callback=?";
        $.getJSON(get_section_number1, function(data){
           $.each(data, function(i,item){
              secnum.push("<option value='" + item + "'>" + item + "</option>"); 
           });
           tagstring = "<select name='sectionnumber1' id= 'sectionnumber1'>" + secnum.join(" ") + "</select>";
           jq("select[name= sectionnumber1]").replaceWith(tagstring);
           jq("input[name= sectionnumber1]").replaceWith(tagstring);
        });                  
    });

    jq("select[name= catalognumber1]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subjects = jq("select[name= subject1]").val();
        var cat1 = jq("select[name= catalognumber1]").val();
        var dash = new String();
        dash = " Please choose ";
        var secnum = new Array(); //array that holds catalog numbers after process
        secnum.push("<option value=" + dash +"'>" + dash + "</option>");
        var get_section_number1 = "https://ws.it.uwosh.edu/getSectionNumbersByTermAndSubjectAndCatalogNumberJSONPCX?strm="+term+"&subject="+subjects+"&catalog_nbr="+cat1+"&callback=?";
        $.getJSON(get_section_number1, function(data){
           $.each(data, function(i,item){
              secnum.push("<option value='" + item + "'>" + item + "</option>"); 
           });
           tagstring = "<select name='sectionnumber1' id= 'sectionnumber1'>" + secnum.join(" ") + "</select>";
           jq("select[name= sectionnumber1]").replaceWith(tagstring);
           jq("input[name= sectionnumber1]").replaceWith(tagstring);
        });                  
    });

    jq("select[name= sectionnumber1]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subjects = jq("select[name= subject1]").val();
        var cat1 = jq("select[name= catalognumber1]").val();
        var sec1 = jq("select[name= sectionnumber1]").val();
        // tag1 = '<input type="text" name="sectionnumber1" class="blurrable firstToFocus" id="sectionnumber1" value="' + sec1 + '" size="30" maxlength="255">';
        // jq("select[name=sectionnumber1]").replaceWith(tag1);
        var get_class_info_URL = "https://ws.it.uwosh.edu/getClassInfoByTermAndSubjectAndCatalogNumberAndSectionJSONPCX?strm="+term+"&subject="+subjects+"&catalog_nbr="+cat1+"&section="+sec1+"&callback=?";
        // expect to get back [10731, "14W", "Paul", "Niesen", "niesen@uwosh.edu"]
        class_number = "TBD.  Please contact the subjects Department";
        instructor_id = "TBD.  No instructor has been assigned to this class as of yet.";
        $.getJSON(get_class_info_URL, function(data){
           $.each(data, function(i,item){
              values = item[0];
              class_number = values[0];
              // alert(class_number);
              instructor_fname = values[2];
              instructor_lname = values[3];
              email = values[4];
              instructor_id = email.slice(0, email.search('@'))
              // alert(instructor_id);
           });
          if (instructor_id ==  "TBD.  No instructor has been assigned to this class as of yet."){
            alert("One of your classes has not yet been assigned an instructor.  Please contact the appropriate department on campus.  Please hit the back button to exit the Time Conflict Card.")
            jq("input class=context[name=form.button.save").hide();
          }  
           tagstring = '<input type="text" name="classnumber1" class="blurrable firstToFocus" id="classnumber1" value="' + class_number + '" size="30" maxlength="255">';
           jq("input[name= classnumber1]").replaceWith(tagstring);
           jq("div[name= classnumber1]").hide();
           jq("input[id= classnumber1]").hide();
           tagstring1 = '<div name="classnumber1fullname" class="blurrable firstToFocus">' + class_number + '</div>';
           jq("input[name= classnumber1]").after(tagstring1);
           jq("div[name= classnumber1fullname]").replaceWith(tagstring1);
           jq("div[name= classnumber1]").replaceWith(tagstring1);
           tagstring2 = '<input type="text" name="instructorID1" class="blurrable firstToFocus" id="instructorID1" value="' + instructor_id + '" size="30" maxlength="255">';
           jq("input[name= instructorID1]").replaceWith(tagstring2);
           jq("input[name= instructorID1]").hide();
           tagstring3 = '<div name="instructorID1fullname" class="blurrable firstToFocus">' + instructor_lname + ', ' + instructor_fname + '</div>';
           jq("input[name= instructorID1]").after(tagstring3);
           jq("div[name= instructorID1fullname]").replaceWith(tagstring3);
           jq("div[name= instructorID1]").replaceWith(tagstring3);
        });        
    });

    jq("select[name= subject2]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subjects2 = jq("select[name= subject2]").val();
        var cat2num = new Array(); //array that holds catalog numbers after process
        var dash = new String();
        dash = " Please choose ";
        cat2num.push("<option value='" + dash +"'>" + dash + "</option>");
        //var catoptions = new String();
        var get_catalog_number = "https://ws.it.uwosh.edu/getCatalogNumbersByTermAndSubjectJSONPCX?strm="+term+"&subject="+subjects2+"&callback=?";
        $.getJSON(get_catalog_number, function(data){
           $.each(data, function(i,item){
               cat2num.push("<option value='" + item + "'>" + item + "</option>"); 
           });
           tagstring = "<select name='catalognumber2' id='catalognumber2'>" + cat2num.join(" ") + "</select>";
           jq("select[name= catalognumber2]").replaceWith(tagstring);
           jq("input[name= catalognumber2]").replaceWith(tagstring);
        });           
    });

    jq("select[name= catalognumber2]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subjects2 = jq("select[name= subject2]").val();
        var cat2 = jq("select[id= catalognumber2]").val();
        // tag2 = '<input type="text" name="catalognumber2" class="blurrable firstToFocus" id="catalognumber2" value="' + cat2 + '" size="30" maxlength="255">';
        // jq("select[name=catalognumber2]").replaceWith(tag2);
        var sec2num = new Array(); //array that holds catalog numbers after process
        var dash = new String();
        dash = "Please choose";
        sec2num.push("<option value='" + dash + "'>" + dash+ "</option>");
        var get_section_number2 = "https://ws.it.uwosh.edu/getSectionNumbersByTermAndSubjectAndCatalogNumberJSONPCX?strm="+term+"&subject="+subjects2+"&catalog_nbr="+cat2+"&callback=?";
        $.getJSON(get_section_number2, function(data){
           $.each(data, function(i,item){
               sec2num.push("<option value='" + item + "'>" + item + "</option>"); 
           });
           tagstring = "<select name='sectionnumber2' id='sectionnumber2'>" + sec2num.join(" ") + "</select>";
           jq("select[name= sectionnumber2]").replaceWith(tagstring);
           jq("input[name= sectionnumber2]").replaceWith(tagstring);
        });           
    });

    jq("select[name= sectionnumber2]").live("change", function(){
        var term = jq("select[name= psterm]").val();
        var subjects = jq("select[name= subject2]").val();
        var cat2 = jq("select[name= catalognumber2]").val();
        var sec2 = jq("select[name= sectionnumber2]").val();
        // tag3 = '<input type="text" name="sectionnumber2" class="blurrable firstToFocus" id="sectionnumber2" value="' + sec2 + '" size="30" maxlength="255">';
        // jq("select[name= sectionnumber2]").replaceWith(tag3);
        var get_class_info_URL = "https://ws.it.uwosh.edu/getClassInfoByTermAndSubjectAndCatalogNumberAndSectionJSONPCX?strm="+term+"&subject="+subjects+"&catalog_nbr="+cat2+"&section="+sec2+"&callback=?";
        // expect to get back [10731, "14W", "Paul", "Niesen", "niesen@uwosh.edu"]
        class_number = "TBD.  Please contact the Department";
        instructor_id = "TBD.  No instructor has been assigned to this class as of yet.";
        $.getJSON(get_class_info_URL, function(data){
           $.each(data, function(i,item){
              values = item[0];
              class_number = values[0];
              // alert(class_number);
              instructor_fname = values[2];
              instructor_lname = values[3];
              email = values[4];
              instructor_id = email.slice(0, email.search('@'))
              // alert(instructor_id);
           });
           if (instructor_id ==  "TBD.  No instructor has been assigned to this class as of yet."){
            alert("One of your classes has not yet been assigned an instructor.  Please contact the appropriate department on campus.  Please hit the back button to exit the Time Conflict Card.")
            jq("input class=context[name=form.button.save").hide();
          }
           tagstring4 = '<input type="text" name="classnumber2" class="blurrable firstToFocus" id="classnumber2" value="' + class_number + '" size="30" maxlength="255">';
           jq("input[name= classnumber2]").replaceWith(tagstring4);
           jq("input[name= classnumber2]").hide();
           tagstring5 = '<div name="classnumber2fullname" class="blurrable firstToFocus">' + class_number + '</div>';
           jq("input[name= classnumber2]").after(tagstring5);
           jq("div[name= classnumber2fullname]").replaceWith(tagstring5);
           jq("div[name= classnumber2]").replaceWith(tagstring5);
           tagstring6 = '<input type="text" name="instructorID2" class="blurrable firstToFocus" id="instructorID2" value="' + instructor_id + '" size="30" maxlength="255">';
           jq("input[name= instructorID2]").replaceWith(tagstring6);
           jq("input[name= instructorID2]").hide();
           tagstring7 = '<div name="instructorID2fullname" class="blurrable firstToFocus">' + instructor_lname + ', ' + instructor_fname + '</div>';
           jq("input[name= instructorID2]").after(tagstring7);
           jq("div[name= instructorID2fullname]").replaceWith(tagstring7);
           jq("div[name= instructorID2]").replaceWith(tagstring7);
        });           
    });
});

