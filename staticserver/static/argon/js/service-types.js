let currentElements = [];
let isUpdate = false;


const currentModal = "#updateServiceTypeModal";
const saveButton = "#serviceTypeSave";
const objectDiv = "#service_types"

const apiUrl = "/api/service/types/";

function loadElements() {
  $.ajax({
    url: apiUrl,
    method: "GET",
    success: function (data) {
      currentElements = data;
      renderElements();
    }
  })
}

function appendElement(index, value) {
  var ServiceTypeElement = `
    <li class="list-group-item border-0 d-flex p-4 ${index >= 1 ? 'mt-3' : ''} mb-2 bg-gray-100 border-radius-lg">
      <div class="d-flex flex-column">
        <h6 class="mb-3 text-sm">Категория: ${value.name}</h6>
      </div>
      <div class="ms-auto text-end">
        <a class="btn btn-link text-danger text-gradient px-3 mb-0" onclick="elementDelete(${value.idx})"><i class="far fa-trash-alt me-2"></i>Удалить</a>
        <a class="btn btn-link text-dark px-3 mb-0" onclick="elementUpdate(${value.idx})"><i class="fas fa-pencil-alt text-dark me-2" aria-hidden="true"></i>Редактировать</a>
      </div>
    </li>
    `;
  $(objectDiv).append(ServiceTypeElement);
}


function renderElements() {
  $(objectDiv).empty();
  for (var i = 0; i < currentElements.length; i++) {
    appendElement(i, currentElements[i]);
  }
}

function elementDelete(idx) {
  if (confirm("Вы уверены что хотите удалить категорию?")) {
    $.ajax({
      url: `${apiUrl}?idx=${idx}`,
      type: "DELETE",
      success: function (response) {
        if (response.status) {
          currentElements = currentElements.filter(element => element.idx !== parseInt(idx));
          renderElements();
        };
      },
      error: function (error) {
        console.error(error);
      }
    });
  }
}

function elementUpdate(idx) {
  $(currentModal).modal("show");
  isUpdate = true;
  let currentElement = currentElements.find(element => element.idx === parseInt(idx));
  $("#serviceTypeIdx").val(currentElement.idx);
  $("#serviceTypeName").val(currentElement.name);
}

function elementSave() {
  const serviceTypeIdx = $("#serviceTypeIdx").val();
  var serviceTypeName = $("#serviceTypeName").val();
  if (!serviceTypeName.length > 0) {
    return alert("Минимум 1 символ!");
  }
  $(saveButton).attr("disabled", "")
  $(saveButton).text("Загрузка...")
  $.ajax({
    url: `${apiUrl}?idx=${serviceTypeIdx}&serviceTypeName=${serviceTypeName}`,
    type: "PUT",
    contentType: false,
    processData: false,
    success: function (response) {
      $(saveButton).removeAttr("disabled");
      $(saveButton).text("Сохранить");
      const updatedServiceType = response.data;
      if (response.status) {
        if (isUpdate) {
          var index = currentElements.findIndex(serviceType => serviceType.idx === updatedServiceType.idx);
          if (index !== -1) {
            currentElements[index] = updatedServiceType;
          }
        } else {
          currentElements.push(updatedServiceType);
        }
        renderElements();
        $(currentModal).modal("hide");
      }
    },
    error: function (error) {
      console.error(error);
    }
  });
}


$(document).ready(function () {
  loadElements();
  $(currentModal).on('hide.bs.modal', function (event) {
    isUpdate = false;
    $("#serviceTypeName").val("");
    $("#serviceTypeIdx").val("");
  })
  $(saveButton).click(e => {
    e.preventDefault();
    elementSave();
  })
});