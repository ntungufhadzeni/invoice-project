$(document).ready(function () {
  calcEditTotal()
  // Attach the input event handler to table inputs
  $("table input").on("input",calcItemTotal);

});

function calcTotal() {
    let sum = 0;
    $(".amount").each(function () {
      sum += parseFloat($(this).text());
    });
    $("#total").text(sum.toFixed(2));
  }

function calcEditTotal() {
    let sum = 0;
    $(".amount").each(function () {
      let $tr = $(this).closest("tr");
      let textValue1 = $("input.rate", $tr).val();
      let textValue2 = $("input.quantity", $tr).val();
      let amt = textValue1 * textValue2;
      $(this, $tr).html(amt.toFixed(2));
      if(amt === 0) $(this).html("");
      sum += amt;
    });
    $("#total").text(sum.toFixed(2));
  }

function calcItemTotal() {
    let $tr = $(this).closest("tr");
    let textValue1 = $("input.rate", $tr).val();
    let textValue2 = $("input.quantity", $tr).val();
    let amt = textValue1 * textValue2;
    $(".amount", $tr).html(amt.toFixed(2));
    calcTotal();
  }

function removeAmount() {
    $(".amount").each(function () {
      let $tr = $(this).closest("tr");
      let textValue1 = $("input.rate", $tr).val();
      let textValue2 = $("input.quantity", $tr).val();
      if(textValue1 === "" && textValue2 === ""){
        $(this).html("");
      }
    });

  }


function cloneMore(selector, prefix) {
  let newElement = $(selector).clone(true);
  let id = `#id_${prefix}-TOTAL_FORMS`
  let total = $(id).val();
  newElement
    .find(":input:not([type=button]):not([type=submit]):not([type=reset])")
    .each(function () {
      let name = $(this).attr("name");
      if (name) {
        name = name.replace("-" + (total - 1) + "-", "-" + total + "-");
        let id = "id_" + name;
        $(this).attr({ name: name, id: id }).val("").prop("checked", false);
      }
    });
  newElement.find("label").each(function () {
    let forValue = $(this).attr("for");
    if (forValue) {
      forValue = forValue.replace("-" + (total - 1) + "-", "-" + total + "-");
      $(this).attr({ for: forValue });
    }
  });
  total++;
  $(id).val(total);
  $(selector).after(newElement);
  removeAmount()
  return false;
}

$(document).ready(function () {
  $(document).on("click", ".add-form-row", function (e) {
    e.preventDefault();
    cloneMore("table tr:last", "form");
    return false;
  });
});

