// set region and zone from church group and zone trigger
cur_frm.add_fetch("church_group", "region", "region");
cur_frm.add_fetch("church_group", "zone", "zone");
cur_frm.add_fetch("zone", "region", "region");