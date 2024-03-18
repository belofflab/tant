arebuild:
	systemctl restart tant
	systemctl restart tant_client

wrebuild:
	systemctl restart tarologueAleksandra
	systemctl restart tarologuePolina
	systemctl restart numerologJulia
	systemctl restart numerologViktoria
	systemctl restart numerologValentina
	systemctl restart numerologNatalia
	systemctl restart numerologKristina
	systemctl restart tarologueKristina

frebuild:
	systemctl restart tant
	systemctl restart tant_client
	systemctl restart tarologueAleksandra
	systemctl restart tarologuePolina
	systemctl restart numerologJulia
	systemctl restart numerologViktoria
	systemctl restart numerologValentina
	systemctl restart numerologNatalia
	systemctl restart numerologKristina
	systemctl restart tarologueKristina