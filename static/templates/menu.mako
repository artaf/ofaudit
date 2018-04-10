<ul class="navbar-nav">

% for id, mitem in menu.items():
    % if mitem[1]:
        <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Menu 3</a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">

        % for sid, smitem in mitem[1].items():
            <a id="index_topmenu${sid}" class="dropdown-item" href="#">${smitem}</a>
        % endfor

        </div>
        </li>
    % else:
        <li class="nav-item">
            <a id="index_topmenu${id}" class="nav-link" href="#">${mitem[0]}</a>
        </li>
    % endif
% endfor

</ul>

<%doc>
        <li class="nav-item active">
            <a class="nav-link" href="#">Menu 1</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#">Menu 2</a>
        </li>
        <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Menu 3</a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                    <a class="dropdown-item" href="#">Menu 3 sub 1</a>
                    <a class="dropdown-item" href="#">Menu 3 sub 2</a>
                    <a class="dropdown-item disabled" href="#">Disabled</a>
                </div>
        </li>
    </ul>
</%doc>
