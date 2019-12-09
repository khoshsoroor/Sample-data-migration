<table class='price-table'>
<tr class='price-table-row-header'>
    % for t in titles:
        <th>${t}</th>
    % endfor
</tr>
    % for item in rows:
        <tr class='price-table-row'>
            % for key in item:
                <td>${item[key]}</td>
            % endfor
        </tr>
    % endfor
</table>