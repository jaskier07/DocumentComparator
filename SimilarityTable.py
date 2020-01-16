from tkinter import W, Button
from tkinter.ttk import Treeview
from tkinter import Toplevel


class SimilarityTable:

    def create(self, arr, filenames, window):
        table_window = Toplevel(window)

        columns = ('File #1', 'File #2', 'Similarity')
        tree = Treeview(table_window, columns=columns, show='headings')
        tree.column('File #1', width=260)
        tree.column('File #2', width=260)
        tree.column('Similarity', width=60)
        tree.grid(row=0, column=0)

        for (i, row) in enumerate(range(1, len(arr))):
            for col in range(0, i + 1):
                similarity = round(arr[row][col], 2)
                tree.insert('', 'end', values=(filenames[row], filenames[col], similarity))

        for col in columns:
            tree.heading(col, text=col, command=lambda: self.sort_by_column(tree, col, False))

    def sort_by_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.sort_by_column(tv, col, not reverse))
