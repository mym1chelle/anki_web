function delete_confirm(e) {
   if(confirm('Вы действительно хотите удалить выбранные записи?')){
            return true;
        }
        else{
            e.preventDefault();
        }
    };


