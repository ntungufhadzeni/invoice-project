$(document).ready(function () {
  // Attach the input event handler to table inputs
  $("table input").on("input", function () {
    let total = [];
    let $tr = $(this).closest("tr");
    let textValue1 = $("input.rate", $tr).val();
    let textValue2 = $("input.quantity", $tr).val();
    let amt = textValue1 * textValue2;
    $(".amount", $tr).html(amt.toFixed(2));
    calc_total();
  });

  function calc_total() {
    let sum = 0;
    $(".amount").each(function () {
      sum += parseFloat($(this).text());
    });
    $("#total").text(sum.toFixed(2));
  }
});

function updateElementIndex(el, prefix, ndx) {
  const id_regex = new RegExp("(" + prefix + "-\\d+)");
  const replacement = prefix + "-" + ndx;
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}


function cloneMore(selector, prefix) {
  let newElement = $(selector).clone(true);
  let total = $("#id_" + prefix + "-TOTAL_FORMS").val();
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
  $("#id_" + prefix + "-TOTAL_FORMS").val(total);
  $(selector).after(newElement);
  return false;
}

$(document).ready(function () {
  $(document).on("click", ".add-form-row", function (e) {
    e.preventDefault();
    cloneMore("table tr:last", "form");
    return false;
  });
});

