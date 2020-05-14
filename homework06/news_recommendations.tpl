<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
            </thead>
            <tbody>
				<tr>
					<td>Интересно:</td>
				</tr>
				%for row in rows:
				%if row['label'] == 'good':
                <tr>
                    <td><a href="{{ row['url'] }}">{{ row['title'] }}</a></td>
                    <td>{{ row['author'] }}</td>
                    <td>{{ row['points'] }}</td>
                    <td>{{ row['comments'] }}</td>
                </tr>
				%end
				%end
				
				<tr>
					<td>Возможно:</td>
				</tr>
				%for row in rows:
				%if row['label'] == 'maybe':
                <tr>
                    <td><a href="{{ row['url'] }}">{{ row['title'] }}</a></td>
                    <td>{{ row['author'] }}</td>
                    <td>{{ row['points'] }}</td>
                    <td>{{ row['comments'] }}</td>
                </tr>
				%end
				%end
				
				<tr>
					<td>Не интересно:</td>
				</tr>
				%for row in rows:
				%if row['label'] == 'never':
                <tr>
                    <td><a href="{{ row['url'] }}">{{ row['title'] }}</a></td>
                    <td>{{ row['author'] }}</td>
                    <td>{{ row['points'] }}</td>
                    <td>{{ row['comments'] }}</td>
                </tr>
				%end
				%end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
