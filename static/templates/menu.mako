<ul class="navbar-nav">

% for id, name in menu.items():
    <li class="nav-item">
        <a class="nav-link" href="#">${name}</a>
    </li>
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
