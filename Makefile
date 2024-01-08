arebuild:
	systemctl restart tant
	systemctl restart tant_client

wrebuild:
	systemctl restart tarologueAleksandra
	systemctl restart tarologuePolina
	systemctl restart tarologueValeria
	systemctl restart numerologViktoria
	systemctl restart numerologValentina
	systemctl restart numerologNatalia

frebuild:
	systemctl restart tant
	systemctl restart tant_client
	systemctl restart tarologueAleksandra
	systemctl restart tarologuePolina
	systemctl restart tarologueValeria
	systemctl restart numerologViktoria
	systemctl restart numerologValentina
	systemctl restart numerologNatalia