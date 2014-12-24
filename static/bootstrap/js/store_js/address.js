    $("#id_address").suggestions({
        serviceUrl: "https://dadata.ru/api/v2",
        token: "c6df49053b76dbaaf973366d8f7b26f718a67638",
        type: "ADDRESS",
	    constraints: {
		    label: "Воронеж",
      // ограничиваем поиск Воронежем и областью
      locations: { region: "воронежская", city: "Воронеж" },
		 deletable: true
    },
    // в списке подсказок не показываем область
    restrict_value: true,
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function(suggestion) {
            console.log(suggestion);
        }
    });