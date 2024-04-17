from typing import Any
from easysnmp import snmp_bulkwalk, snmp_get
from easysnmp.session import SNMPVariableList, SNMPVariable


def bulk_walk(**kwargs) -> list[Any]:
    s_l: SNMPVariableList[SNMPVariable] = snmp_bulkwalk(**kwargs)
    return [i.value for i in s_l]


def get(**kwargs) -> Any:
    s: SNMPVariable = snmp_get(**kwargs)
    return s.value
