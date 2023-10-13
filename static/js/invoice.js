$(document).ready(function () {
  calcEditTotal();
  changeBtn();

  // Attach the input event handler to table inputs
  $("table").on("input", "input", function () {
    if ($(this).hasClass("rate") || $(this).hasClass("quantity")) {
      calcItemTotal.call(this);
    }
  });

  $(document).on("click", ".add-form-row", function (e) {
    e.preventDefault();
    cloneMore("table tr:last", "form");
    return false;
  });

  $(document).on('click', '.remove-form-row', function (e) {
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
  });
});

function calcTotal() {
  let sum = 0;
  $(".amount").each(function () {
    sum += parseFloat($(this).text()) || 0;
  });
  $("#total").text(sum.toFixed(2));
}

function calcEditTotal() {
  let sum = 0;
  $(".amount").each(function () {
    let $tr = $(this).closest("tr");
    let textValue1 = parseFloat($("input.rate", $tr).val()) || 0;
    let textValue2 = parseFloat($("input.quantity", $tr).val()) || 0;
    let amt = textValue1 * textValue2;
    $(this).html(amt ? amt.toFixed(2) : "");

    sum += amt;
  });
  $("#total").text(sum.toFixed(2));
}

function calcItemTotal() {
  let $tr = $(this).closest("tr");
  let textValue1 = parseFloat($("input.rate", $tr).val()) || 0;
  let textValue2 = parseFloat($("input.quantity", $tr).val()) || 0;
  let amt = textValue1 * textValue2;
  $(".amount", $tr).html(amt ? amt.toFixed(2) : "");
  calcTotal();
}

function removeAmount() {
  $(".amount").each(function () {
    let $tr = $(this).closest("tr");
    let textValue1 = parseFloat($("input.rate", $tr).val()) || 0;
    let textValue2 = parseFloat($("input.quantity", $tr).val()) || 0;

    if (textValue1 === 0 && textValue2 === 0) {
      $(this).html("");
    }
  });
}

function updateElementIndex(el, prefix, ndx) {
  const id_regex = new RegExp("(" + prefix + "-\\d+)");
  const replacement = prefix + "-" + ndx;
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix) {
  let newElement = $(selector).clone(true);
  let elId = `#id_${prefix}-TOTAL_FORMS`;
  let total = $(elId).val();
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
  $(elId).val(total);
  $(selector).after(newElement);
  removeAmount();
  changeBtn();
  return false;
}

function deleteForm(prefix, btn) {
  let elId = `#id_${prefix}-TOTAL_FORMS`
  const total = parseInt($(elId).val());
  if (total > 1) {
    btn.closest('.form-row').remove();
    const forms = $('.form-row');
    $(elId).val(forms.length);
    let i = 0, formCount = forms.length;
    for (; i < formCount; i++) {
      $(forms.get(i)).find(':input').each(function () {
        updateElementIndex(this, prefix, i);
      });
    }
  }
  calcEditTotal();
  return false;
}

function changeBtn() {
  const conditionRow = $('.form-row:not(:last)');
  conditionRow.find('a.add-form-row')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('<i class="fa-regular fa-square-minus has-text-danger fa-2x"></i>');
}
