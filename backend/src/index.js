import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

// Define your GraphQL schema
const typeDefs = gql`
    type Query {
        hello: String
    }
`;

// Define your resolver functions
const resolvers = {
    Query: {
        hello: () => 'Hello, world!'
    }
};

const server = new ApolloServer({
    typeDefs,
    resolvers
});

const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 }
});
console.log(url)