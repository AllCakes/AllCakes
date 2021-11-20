
   /* When the user clicks on the button, 
   toggle between hiding and showing the dropdown content */
   function myFunction() {
      console.log("action")
      document.getElementById("myDropdown").classList.toggle("showw");
   }

   function myFunction1() {
      console.log("action")
      document.getElementById("myDropdown").classList.toggle("showw");
      //이벤트가 데려오는 타켓은 myDropdown
   }
   /* 서울 */

   function myFunction2() {
      console.log("action2")
      document.getElementById("myDropdown2").classList.add("showw");
   }

   function myFunction3() {
      console.log("action2")
      document.getElementById("myDropdown2").classList.toggle("showw");
   }

   /* 경기 */
   function myFunction4() {
      console.log("action3")
      document.getElementById("myDropdown3").classList.toggle("showw");
   }


   function myFunction5() {
      console.log("action3")
      document.getElementById("myDropdown3").classList.toggle("showw");
   }

   /*인천*/

   function myFunction6() {
      console.log("action")
      document.getElementById("myDropdown4").classList.toggle("showw");
   }


   function myFunction7() {
      console.log("action")
      document.getElementById("myDropdown4").classList.toggle("showw");
   }

   /*대전*/
   function myFunction8() {
      console.log("action")
      document.getElementById("myDropdown5").classList.toggle("showw");
   }


   function myFunction9() {
      console.log("action")
      document.getElementById("myDropdown5").classList.toggle("showw");
   }

   /*대전*/

   function myFunction10() {
      console.log("action")
      document.getElementById("myDropdown6").classList.toggle("showw");
   }


   function myFunction11() {
      console.log("action")
      document.getElementById("myDropdown6").classList.toggle("showw");
   }


   function myFunction12() {
      console.log("action")
      document.getElementById("myDropdown7").classList.toggle("showw");
   }


   function myFunction13() {
      console.log("action")
      document.getElementById("myDropdown7").classList.toggle("showw");
   }


   function myFunction14() {
      console.log("action")
      document.getElementById("myDropdown8").classList.toggle("showw");
   }


   function myFunction15() {
      console.log("action")
      document.getElementById("myDropdown8").classList.toggle("showw");
   }


   function myFunction16() {
      console.log("action")
      document.getElementById("myDropdown9").classList.toggle("showw");
   }


   function myFunction17() {
      console.log("action")
      document.getElementById("myDropdown9").classList.toggle("showw");
   }


   function myFunction18() {
      console.log("action")
      document.getElementById("myDropdown10").classList.toggle("showw");
   }


   function myFunction19() {
      console.log("action")
      document.getElementById("myDropdown10").classList.toggle("showw");
   }


   function myFunction20() {
      console.log("action")
      document.getElementById("myDropdown11").classList.toggle("showw");
   }


   function myFunction21() {
      console.log("action")
      document.getElementById("myDropdown11").classList.toggle("showw");
   }


   function myFunction22() {
      console.log("action")
      document.getElementById("myDropdown12").classList.toggle("showw");
   }


   function myFunction23() {
      console.log("action")
      document.getElementById("myDropdown12").classList.toggle("showw");
   }


   function myFunction24() {
      console.log("action")
      document.getElementById("myDropdown13").classList.toggle("showw");
   }


   function myFunction25() {
      console.log("action")
      document.getElementById("myDropdown13").classList.toggle("showw");
   }


   function myFunction26() {
      console.log("action")
      document.getElementById("myDropdown14").classList.toggle("showw");
   }


   function myFunction27() {
      console.log("action")
      document.getElementById("myDropdown14").classList.toggle("showw");
   }


   function myFunction28() {
      console.log("action")
      document.getElementById("myDropdown15").classList.toggle("showw");
   }


   function myFunction29() {
      console.log("action")
      document.getElementById("myDropdown15").classList.toggle("showw");
   }


   function myFunction30() {
      console.log("action")
      document.getElementById("myDropdown16").classList.toggle("showw");
   }


   function myFunction31() {
      console.log("action")
      document.getElementById("myDropdown16").classList.toggle("showw");
   }


   function myFunction32() {
      console.log("action")
      document.getElementById("myDropdown17").classList.toggle("showw");
   }


   function myFunction33() {
      console.log("action")
      document.getElementById("myDropdown17").classList.toggle("showw");
   }




   // Close the dropdown if the user clicks outside of it
   onclick = function (event) {
      if (!event.target.matches('.dropbtn') && !event.target.matches('.contentbtn')) {

         console.log("btn clicked")
         var dropdowns = document.getElementsByClassName("dropdown-content");
         var i;
         for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('showw')) {
               openDropdown.classList.remove('showw');
            }
         }
      }
   }
