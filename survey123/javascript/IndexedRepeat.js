function indexed_repeat(name, grp, i, subgrp, subi, subsubgrp, subsubi) {
    let outValue = null;
    if (name == undefined || !Array.isArray(grp) || !Number.isInteger(i) || i > grp.length || i < 1) {
        return outValue;
    }
    if (subgrp != undefined && Number.isInteger(subi) && subi < grp[i - 1][subgrp].length && subi > 0) {
        if (subsubgrp != undefined && Number.isInteger(subsubi) && subsubi < grp[i - 1][subgrp][subi - 1][subsubgrp].length && subsubi > 0) {
            outValue = grp[i - 1][subgrp][subi - 1][subsubgrp][subsubi - 1][name];
        } else {
            // return JSON.stringify(grp)
            outValue = grp[i - 1][subgrp][subi - 1][name];
        }
    } else {
        outValue = grp[i - 1][name];
    }

    return outValue
}
