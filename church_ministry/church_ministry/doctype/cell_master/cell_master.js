// set region and zone from church group and zone trigger

cur_frm.add_fetch("senior_cell", "pcf", "pcf");
cur_frm.add_fetch("senior_cell", "church", "church");
cur_frm.add_fetch("senior_cell", "church_group", "church_group");
cur_frm.add_fetch("senior_cell", "region", "region");
cur_frm.add_fetch("senior_cell", "zone", "zone");


cur_frm.add_fetch("pcf", "church", "church");
cur_frm.add_fetch("pcf", "church_group", "church_group");
cur_frm.add_fetch("pcf", "region", "region");
cur_frm.add_fetch("pcf", "zone", "zone");

cur_frm.add_fetch("church", "church_group", "church_group");
cur_frm.add_fetch("church", "region", "region");
cur_frm.add_fetch("church", "zone", "zone");

cur_frm.add_fetch("church_group", "region", "region");
cur_frm.add_fetch("church_group", "zone", "zone");

cur_frm.add_fetch("zone", "region", "region");