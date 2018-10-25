<script>
function filter() {
  var dropdown, selected_person, input, filter, ul, li, a, i;
  dropdown = document.getElementById("name_select");
  selected_person = dropdown.value;
  input = document.getElementById("searchbar");
  filter = input.value.toUpperCase();
  selector = document.getElementById("selector");
  a = selector.getElementsByTagName("li");
  for (i = 0; i < a.length; i++) {
    if (a[i].innerHTML.toUpperCase().indexOf(filter) === -1 || a[i].getElementsByTagName("input")[0].value === selected_person) {
      a[i].style.display = "none";
    } else {
      a[i].style.display = "";
    }
  }
}
</script>
